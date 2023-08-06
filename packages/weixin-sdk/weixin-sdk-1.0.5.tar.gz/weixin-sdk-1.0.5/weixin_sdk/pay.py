#-*- coding: utf-8 -*-

from utils import HttpUtil, Util


class WxPay(object):

    """
    微信支付相关接口, 考虑NATIVE和JSAPI和APP支付
    """

    BASE_URL = 'https://api.mch.weixin.qq.com'

    def __init__(self, appid, mch_id, sign_key, cert=None):
        """
        初始化支付对象
        :param appid: 公众号appid(JSAPI和NATIVE), 开放平台appid(APP)
        :param mch_id: 商户id
        :param sign_key: 商户签名密钥
        :param cert: 商户证书文件,tuple:
                     (apiclient_cert.pem路径, apiclient_key.pem路径),
                     涉及到资金回滚的接口需要
        """
        self._appid = appid
        self._mchid = mch_id
        self._sign_key = sign_key
        self._cert = cert

    def unified_order(self, trade_type, out_trade_no, body,
                      total_fee, notify_url, **kwargs):
        """
        微信统一下单api(文档http://pay.weixin.qq.com/wiki/doc/api/index.php?chapter=9_1)
        :param trade_type: 交易类型('JSAPI', 'APP', 'NATIVE')
        :param out_trade_no: 商户订单号,32个字符内
        :param body: 商品或支付简单描述
        :param total_fee: 金额(分),默认RMB,需要其他货币类型在kwargs内指定
        :param notify_url: 支付结果通知地址
        :return: 返回tuple(code, result), 统一下单结果
        """
        if not trade_type:
            raise WxPayError(u"缺少统一支付接口必填参数trade_type！")
        if not out_trade_no:
            raise WxPayError(u"缺少统一支付接口必填参数out_trade_no！")
        if not body:
            raise WxPayError(u"缺少统一支付接口必填参数body！")
        if not total_fee:
            raise WxPayError(u"缺少统一支付接口必填参数total_fee！")
        if not notify_url:
            raise WxPayError(u"异步通知url未设置")

        #检查ip
        if not kwargs.get('spbill_create_ip'):
            if trade_type == 'NATIVE':
                kwargs.update(spbill_create_ip=Util.get_local_ip())
            else:
                raise WxPayError(u'APP和网页支付需提交用户端ip')

        if trade_type == 'NATIVE':
            assert kwargs.get('product_id'), u'trade_type为NATIVE时，product_id为必填参数'
        elif trade_type == 'JSAPI':
            assert kwargs.get('openid'), u'trade_type为JSAPI时，openid为必填参数！'
        elif trade_type == 'APP':
            pass
        else:
            raise WxPayError(u"支付类型trade_type错误,为('JSAPI', 'APP', 'NATIVE')之一")

        kwargs.update(device_info='WEB')

        kwargs.update(appid=self._appid, mch_id=self._mchid)
        kwargs.update(trade_type=trade_type,
                      out_trade_no=out_trade_no,
                      body=body,
                      total_fee=total_fee,
                      notify_url=notify_url)
        kwargs.update(nonce_str=Util.generate_nonce(20))

        kwargs.update(sign=self._generate_sign(**kwargs)) #sign

        return self._post('/pay/unifiedorder', kwargs)


    def query_order(self, transaction_id='', out_trade_no=''):
        """
        查询订单api, 文档(http://pay.weixin.qq.com/wiki/doc/api/index.php?chapter=9_2)
        :param transaction_id: 微信订单号, 优先
        :param out_trade_no: 商户内部订单号
        :return 返回tuple(code, result)
        """
        if not (transaction_id or out_trade_no):
            raise WxPayError(u"订单查询接口中，out_trade_no、transaction_id至少填一个")

        kwargs = {'appid':self._appid, 'mch_id':self._mchid}
        kwargs.update(transaction_id=transaction_id, out_trade_no=out_trade_no)
        kwargs.update(nonce_str=Util.generate_nonce(20))

        kwargs.update(sign=self._generate_sign(**kwargs))  #sign

        return self._post('/pay/orderquery', kwargs)


    def close_order(self, out_trade_no):
        """
        关闭交易
        :param out_trade_no: 商户订单号
        :return: 返回tuple(code, result)
        """
        if not out_trade_no:
            raise WxPayError("订单查询接口中，out_trade_no必填！")

        kwargs = {'appid':self._appid, 'mch_id':self._mchid}
        kwargs.update(out_trade_no=out_trade_no)
        kwargs.update(nonce_str=Util.generate_nonce(20))

        kwargs.update(sign=self._generate_sign(**kwargs))  #sign

        return self._post('/pay/closeorder', kwargs)


    def refund(self, out_refund_no, total_fee, refund_fee,
               transaction_id='', out_trade_no='', **kwargs):
        """
        退款,请求需要双向证书
        """
        if not out_refund_no:
            raise WxPayError(u"退款申请接口中，缺少必填参数out_refund_no(商户系统内部退款单号)！")
        if not total_fee:
            raise WxPayError(u"退款申请接口中，缺少必填参数total_fee(订单总金额，单位为分, 整数)！")
        if not refund_fee:
            raise WxPayError(u"退款申请接口中，缺少必填参数refund_fee(退款金额，单位为分, 整数)！")
        if not (transaction_id or out_trade_no):
            raise WxPayError(u"订单查询接口中，out_trade_no、transaction_id至少填一个")

        kwargs.update(
            appid=self._appid,
            mch_id=self._mchid,
            out_refund_no=out_refund_no,
            total_fee=total_fee,
            refund_fee=refund_fee,
            transaction_id=transaction_id,
            out_trade_no=out_trade_no,
            nonce_str=Util.generate_nonce(20),
            op_user_id=self._mchid
        )

        kwargs.update(sign=self._generate_sign(**kwargs))  #sign

        return self._post('/secapi/pay/refund', kwargs, need_cert=True)


    def query_refund(self, transaction_id='', out_trade_no='',
                     out_refund_no='', refund_id='', **kwargs):
        """
        查询退款, 参数四选一
        """
        if not (transaction_id and out_refund_no and out_trade_no, refund_id):
            raise WxPayError(u"订单查询接口中，transaction_id and out_refund_no and out_trade_no, refund_id至少填一个")

        kwargs.update(
            appid=self._appid,
            mch_id=self._mchid,
            nonce_str=Util.generate_nonce(20),
            transaction_id=transaction_id,
            out_refund_no=out_refund_no,
            out_trade_no=out_trade_no,
            refund_id=refund_id
        )
        kwargs.update(sign=self._generate_sign(**kwargs))  #sign

        return self._post('/pay/refundquery', kwargs, need_cert=True)


    def parse_notify_result(self, body):
        """
        微信服务器通知支付结果时使用
        将request body的xml格式转为dict,签名错误时返回None
        """
        dresult = Util.xml_to_dict(body)
        if self._generate_sign(**dresult) != dresult.get('sign'):
            return None
        return dresult

    def pack_notify_response(self, return_code='SUCCESS', return_msg='OK'):
        """将支付结果通知请求的响应结果打包成xml"""
        return Util.dict_to_xml({'return_code':return_code, 'return_msg':return_msg})

    def sign_for_jspay(self, prepay_id):
        """jssdk调起支付时需要的sign"""
        timestamp = Util.timestamp()
        nonce_str = Util.generate_nonce(15)
        package = 'prepay_id=%s' % prepay_id
        sign_type = 'MD5'
        pay_sign = self._generate_sign(appId=self._appid, timeStamp=timestamp,
                                nonceStr=nonce_str, package=package, signType=sign_type)
        return {'timestamp':timestamp, 'nonceStr':nonce_str, 'package':package, 'signType':sign_type, 'paySign':pay_sign}

    def _generate_sign(self, **kwargs):
        """
        签名算法,返回得到的签名字符串
        """
        valid_keys = [k for k in kwargs if kwargs[k] and k != 'sign']
        valid_keys.sort()
        kv_str = ''
        for k in valid_keys:
            kv_str += '%s=%s&' % (k, kwargs[k])
        kv_str += '%s=%s' % ('key', self._sign_key)
        kv_str = Util.encode_data(kv_str)
        sign = Util.md5(kv_str).upper()
        return sign


    def _post(self, url, ddata, need_cert=False):
        if need_cert:
            if not self._cert:
                raise WxPayError(u"该接口需要双向证书")
            else:
                verify_cert = self._cert
        else:
            verify_cert = None
        return self._common_post(url, ddata, cert=verify_cert)

    def _common_post(self, url, ddata, cert=None):
        """
        :return: (ret_code, dict_data/err_msg)
        """
        if self.BASE_URL not in url:
            url = self.BASE_URL + url
        results = HttpUtil.post(url, ddata, ctype='xml', cert=cert)

        if results.get('return_code', '') == 'SUCCESS':
            assert results.get('sign') == self._generate_sign(**results), 'sign error, not from wechat pay server'
            if results.get('result_code','') == 'SUCCESS':
                return 0, results
            else:
                return 1, results.get('err_code_des', '')
        else:
            return 1,results.get('return_msg', '')



class WxPayError(Exception):
    pass


if __name__ == "__main__":
    pass
