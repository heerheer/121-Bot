import requests

def query_electric_bill(jsessionid, sysid=2, roomNo=4372, elcarea=2, elcbuis=4355):
    url = "http://202.195.206.214/epay/electric/queryelectricbill"
    headers = {
        "Cookie": 'JSESSIONID='+jsessionid
    }
    data = {
        "sysid": sysid,
        "roomNo": roomNo,
        "elcarea": elcarea,
        "elcbuis": elcbuis
    }
    
    try:
        response = requests.post(url, headers=headers, data=data)

        response.raise_for_status()  # 如果响应状态码不是200，会抛出异常
        result = response.json()
        
        if result.get("retcode") == 0:
            return result.get("restElecDegree", 0)
        else:
            return 0
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return 0
