
import os
import requests

CHATGPT_ENGINE = os.environ["CHATGPT_ENGINE"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]


def chatgpt_response(messages, persona, temperature=0.5):
    messages.insert(0, {"role": "system", "content": persona})
    url = 'https://api.openai.com/v1/chat/completions'
    data = {
        "model": CHATGPT_ENGINE,
        "messages": messages,
        "temperature": temperature,
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENAI_API_KEY}',
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        result = response.json()
        answer = result['choices'][0]['message']['content']
        return answer
    except (KeyError, IndexError) as e:
        return "GPT3 Return Error: " + str(e)
    except Exception as e:
        return "GPT3 Error: " + str(e)


def summary(text):
    persona = "당신은 글읽기 요약을 잘하는 최고의 시스템입니다."
    messages = [{"role": "user",
                 "content": f"아래 뉴스 내용을 쉽게 파악할수 있도록 한두즐로 요약해주세요: \n\n{text}"}]
    return chatgpt_response(messages, persona, temperature=0.1)


if __name__ == "__main__":
    print(summary("""넷플릭스 오리지널 시리즈 '더 글로리' 파트2 공개 당일 국내 넷플릭스 앱을 이용한 사람들이 하루 사이 55% 폭증한 것으로 나타났습니다.
아이지에이웍스의 빅데이터 솔루션 모바일인덱스는 오늘(13일) 넷플릭스 앱의 플레이스토어·애플 앱스토어 합산 일간 활성 이용자가 지난 10일 474만8천605명으로 집계됐다고 밝혔습니다.

전날인 지난 9일 305만1천798명보다 55.6% 증가한 것입니다.

일주일 전인 지난 3일(257만4천327명)보다는 84.5% 늘었습니다.

1인당 넷플릭스 앱 평균 사용 시간은 83.53분으로, 지난 9일 63.28분과 지난 3일 62.37분을 크게 뛰어넘었습니다.

이용자와 사용 시간 모두 아이지에이웍스가 양대 앱 마켓 합산으로 모바일인덱스 분석을 시작한 2020년 5월 이후 최대치입니다.

파트1(1∼8회)에 열광하며 파트2를 손꼽아 기다렸던 국내외 시청자들이 공개 당일 일제히 '몰아보기'에 나선 것으로 해석됩니다.
"""))
