import os
import requests
import datetime
import xmltodict
from weather_data import MAP_DATA, SKY_PTY_DATA, DAY_DATA

WEATHER_API_KEY = os.environ["WEATHER_API_KEY"]
TODAY = datetime.datetime.now()
# TODAY = datetime.datetime(2023,3,17)

def make_tilde_expression(list_value, unit):
    list_value = [float(i) for i in list_value]
    min_value = min(list_value)
    max_value = max(list_value)
    if min_value == max_value:
        return str(min_value) + unit
    else:
        return str(min_value) + unit + '~' + str(max_value) + unit


def get_weather_api_result():
    #get weather data of location
    result_dict = dict()
    for i in MAP_DATA.keys():
        option = {
            "serviceKey":WEATHER_API_KEY,
            "dataType":"JSON",
            "pageNo":1,
            "numOfRows":1000,
            "base_date":TODAY.strftime("%Y%m%d"),
            "base_time":"0200",
            "nx":str(MAP_DATA[i]['nx']),
            "ny":str(MAP_DATA[i]['ny'])
        }
        url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
        try:
            response = requests.get(url, params=option)
            res = response.json()["response"]["body"]["items"]['item']
        except KeyError:
            print(response.content)
        except requests.exceptions.JSONDecodeError:
            print(xmltodict.parse(response.content))
        result_list = []
        for j in res:
            #PTY: 강수 형태, SKY: 하늘 상태, TMN: 최저 기온, TMX: 최고 기온
            if j['category'] in ["PTY", "SKY", "TMN", "TMX"]:
                result_list.append(j)
        result_dict[i] = result_list

    return result_dict


def make_weather_dict(result_dict):
    total_result_dict = dict()
    for city in list(MAP_DATA.keys()):
        local_result_dict = {
            '오늘' : "",
            '내일' : "",
            '모레' : ""
        }
        for j in [0, 1, 2]:
            morning_pty_list = []
            morning_sky_list = []
            afternoon_pty_list = []
            afternoon_sky_list = []
            temprature_list = []
            for i in result_dict[city]:
                if i['fcstDate'] == (TODAY + datetime.timedelta(days=j)).strftime("%Y%m%d"):
                    if i['fcstTime'] < '1200':
                        if i['category'] == "TMN":
                            temprature_list.append(i['fcstValue'])
                        elif i['category'] == "PTY":
                            morning_pty_list.append(i['fcstValue'])
                        elif i['category'] == "SKY":
                            morning_sky_list.append(i['fcstValue'])
                    elif i['fcstTime'] >= '1200':
                        if (i['category'] == "TMX"):
                            temprature_list.append(i['fcstValue'])
                        elif i['category'] == "PTY":
                            afternoon_pty_list.append(i['fcstValue'])
                        elif i['category'] == "SKY":
                            afternoon_sky_list.append(i['fcstValue'])
            local_result_dict[DAY_DATA[j]] += make_tilde_expression(temprature_list, '°C')
            if SKY_PTY_DATA[max(morning_sky_list)][max(morning_pty_list)] == SKY_PTY_DATA[max(afternoon_sky_list)][max(afternoon_pty_list)]:
                local_result_dict[DAY_DATA[j]] += (" 종일-" + SKY_PTY_DATA[max(morning_sky_list)][max(morning_pty_list)])
            else:
                local_result_dict[DAY_DATA[j]] += (" 오전-" + SKY_PTY_DATA[max(morning_sky_list)][max(morning_pty_list)])
                local_result_dict[DAY_DATA[j]] += (" 오후-" + SKY_PTY_DATA[max(afternoon_sky_list)][max(afternoon_pty_list)])
        total_result_dict[city] = local_result_dict

        #order is important
        weather_dict = dict()
        weather_dict["전국"] = total_result_dict["서울 인천 경기"]
        for i in total_result_dict.keys():
            weather_dict[i] = total_result_dict[i]

        return weather_dict


def make_weather_prompt(weather_dict):
    weather_string = str(weather_dict)
    weather_string = weather_string.replace("'",'')[1:-1]
    #make system prompt for weather chatgpt
    weather_prompt = f"당신은 기상 캐스터입니다. 아래의 사전 형태의 기상 정보에 기반해서, 날씨를 묻는 질문에 기상 예보처럼 자연스럽게 답해주세요.\n{weather_string}\n답변에 최저 기온과 최대 기온을 포함해주세요. 잘 모르겠으면 전국 정보를 알려주세요."

    return weather_prompt

if __name__ == "__main__":
    weather_api_result = get_weather_api_result()
    weather_dict = make_weather_dict(weather_api_result)
    weather_prompt = make_weather_prompt(weather_dict)

    # Print the text
    print(weather_prompt)