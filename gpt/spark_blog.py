# pip install --upgrade spark_ai_python

from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
import re
import json
import requests
from config import SPARKAI_URL, SPARKAI_APP_ID, SPARKAI_API_SECRET, SPARKAI_API_KEY, SPARKAI_DOMAIN, \
    SPARKAI_Authorization, SPARKAI_HTTP_URL, TOPIC_THRESHOLDS
import logging


def websocket_no_stream(bio, blog_html):
    """

    :return:
    """
    spark = ChatSparkLLM(
        spark_api_url=SPARKAI_URL,
        spark_app_id=SPARKAI_APP_ID,
        spark_api_key=SPARKAI_API_KEY,
        spark_api_secret=SPARKAI_API_SECRET,
        spark_llm_domain=SPARKAI_DOMAIN,
        streaming=False,
    )
    messages = [
        ChatMessage(
            role="system",
            content='你现在是一名计算机领域的技术顾问，能够准确且简洁的回答用户的问题。'
        ),
        ChatMessage(
            role="user",
            content='用户简介:{}。用户博客网页爬取的内容:{}。请你根据上述信息，给这个用户的开发能力打分，满分100分。不要看html内容的长度，要根据内容的技术程度。如果是全是生活博客，开发者能力分数就很低，如果是是技术分享博客，则根据内容的图文丰富性和技术研究的深入程度，进行评分。结果用数字输出，例如输出:43分。'.format(
                bio, blog_html)
        )
    ]
    handler = ChunkPrintHandler()
    a = spark.generate([messages], callbacks=[handler])
    output = a.generations[0][0].text
    number = re.findall(r'\d+', output)
    if number:
        blog_score = int(number[0])
    else:
        blog_score = 0
    return blog_score






def http_no_stream(bio, blog_html):
    url = SPARKAI_HTTP_URL
    data = {
        "max_tokens": 30,
        "top_p": 0.8,
        "top_k": 1,
        "temperature": 0.5,
        "presence_penalty": 1,
        "messages": [
            {
                "role": "system",
                "content": "你现在是一名计算机领域的技术顾问，能够准确且简洁的回答用户的问题。"
            },
            {
                "role": "user",
                "content": "用户简介:{}。用户博客网页爬取的内容:{}。请你根据上述信息，给这个用户的开发能力打分，满分100分。根据内容的技术程度。如果是生活记录博客，开发者能力分数就很低，如果是是技术分享博客，则根据内容的图文丰富性和技术研究的深入程度，进行评分。结果用数字输出，例如输出:43分。然后给出理由，为什么得到这个分数，是由哪些信息相加得到的".format(
                    bio, blog_html)
            }
        ],
        "model": "lite"
    }
    data["stream"] = False
    # 我的鉴权信息
    header = {
        "Authorization": SPARKAI_Authorization
    }
    response = requests.post(url, headers=header, json=data)

    # 大模型流式响应解析示例，data["stream"] = True
    # response.encoding = "utf-8"
    # for line in response.iter_lines(decode_unicode="utf-8"):
    #     print(line)

    # 非流式:大模型生成完，再一次性返回
    output_json = json.loads(response.text)

    if 'code' in output_json and output_json['code'] != 0:  # 错误
        code = output_json['code']
        logging.error(f'请求错误: {code},{output_json}')
        return ""  # 大模型非正常输出，返回空     #====
    elif 'code' in output_json and output_json['code'] == 0:  # 正确
        output = output_json['choices'][0]['message']['content']
        print(output)
        number = re.findall(r'\d+', output)
        if number:
            blog_score = int(number[0])
        else:
            blog_score = 0
        return blog_score

    elif 'error' in output_json:
        logging.error(output_json)
        return []


if __name__ == '__main__':
    """

    传入3个参数：bio，blog_html
    """
    bio = ""
    blog_html = """<body>
  <header>
    <h1>RReverser's</h1>
    
    <nav>
      <ul>
        <li><a href="/" rel="home">Home</a></li>
        <li><a href="/posts/">Archive</a></li>
        <li><a href="/about/" rel="author">About Me</a></li>
      </ul>
    </nav>
  </header>

  <main>
    

<h2>Latest 10 Posts</h2>



<ol reversed start="102">

  <li>
    <a href="https://blog.stackblitz.com/posts/bringing-sharp-to-wasm-and-webcontainers/">Bringing Sharp to WebAssembly and WebContainers</a>
    <time datetime="2023-08-03">03 Aug 2023</time>
    
    <br>
    <em>Challenges of porting native Node.js modules like Sharp to more platforms with WebAssembly.</em>
  </li>

  <li>
    <a href="https://github.com/RReverser/serde-ndim">Github project: serde-ndim</a>
    <time datetime="2023-04-02">02 Apr 2023</time>
    
    <br>
    <em>Serde support for n-dimensional arrays from self-describing formats</em>
  </li>

  <li>
    <a href="https://github.com/RReverser/ascom-alpaca-rs">Github project: ascom-alpaca-rs</a>
    <time datetime="2023-03-18">18 Mar 2023</time>
    
    <br>
    <em>Cross-platform Rust library for the ASCOM Alpaca API for astronomy devices</em>
  </li>

  <li>
    <a href="https://github.com/RReverser/eos-remote-web">Github project: eos-remote-web</a>
    <time datetime="2023-02-27">27 Feb 2023</time>
    
    <br>
    <em>Web Bluetooth remote for Canon EOS cameras</em>
  </li>

  <li>
    <a href="https://web.dev/articles/drawing-to-canvas-in-emscripten">Drawing to canvas in Emscripten</a>
    <time datetime="2022-02-07">07 Feb 2022</time>
    
    <br>
    <em>Learn how to render 2D graphics to a canvas on the web from WebAssembly with Emscripten.</em>
  </li>

  <li>
    <a href="https://web.dev/articles/porting-gphoto2-to-the-web">Porting USB applications to the web. Part 2: gPhoto2</a>
    <time datetime="2022-02-01">01 Feb 2022</time>
    
    <br>
    <em>Learn how gPhoto2 was ported to WebAssembly to control external cameras over USB from a web app.</em>
  </li>

  <li>
    <a href="https://web.dev/articles/webassembly-feature-detection">WebAssembly feature detection</a>
    <time datetime="2022-01-27">27 Jan 2022</time>
    
    <br>
    <em>Learn how to use the newest WebAssembly features while supporting users across all browsers.</em>
  </li>

  <li>
    <a href="https://web.dev/articles/porting-libusb-to-webusb">Porting USB applications to the web. Part 1: libusb</a>
    <time datetime="2022-01-20">20 Jan 2022</time>
    
    <br>
    <em>Learn how code that interacts with external devices can be ported to the web with WebAssembly and Fugu APIs.</em>
  </li>

  <li>
    <a href="https://web.dev/articles/emscripten-embedding-js-snippets">Embedding JavaScript snippets in C++ with Emscripten</a>
    <time datetime="2022-01-18">18 Jan 2022</time>
    
    <br>
    <em>Learn how to embed JavaScript code in your WebAssembly library to communicate with the outside world.</em>
  </li>

  <li>
    <a href="https://web.dev/articles/bundling-non-js-resources">Bundling non-JavaScript resources</a>
    <time datetime="2021-09-08">08 Sep 2021</time>
    
    <br>
    <em>Learn how to import and bundle various types of assets from JavaScript in a way that works both in browsers and bundlers.</em>
  </li>

</ol>


<p>More posts can be found in <a href="/posts/">the archive</a>.</p>


  </main>

  <footer>
    <p><a href="https://simplecss.org">Simple.css</a> was created by <a href="https://kevq.uk">Kev Quirk</a> and is licensed under the MIT license.</p>
    <p>Starter template by <a href="https://www.lkhrs.com">Luke Harris</a>.</p>
  </footer>

  <!-- Current page: / -->
<!-- Cloudflare Pages Analytics --><script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{"token": "afadb0dcb5a446ba97328fbf549320f1"}'></script><!-- Cloudflare Pages Analytics --><script defer src="https://static.cloudflareinsights.com/beacon.min.js/vcd15cbe7772f49c399c6a5babf22c1241717689176015" integrity="sha512-ZpsOmlRQV6y907TI0dKBHq9Md29nnaEIPlkf84rnaERnq6zvWvPUqr2ft8M1aS28oN72PdrCzSjY4U6VaAw1EQ==" data-cf-beacon='{"rayId":"8dc5cff55f2f1015","serverTiming":{"name":{"cfExtPri":true,"cfL4":true,"cfSpeedBrain":true,"cfCacheStatus":true}},"version":"2024.10.4","token":"3203adb19f044d85a51a7bd856c7d0dd"}' crossorigin="anonymous"></script>
</body>
    """

    # # Websocket的方式
    # predict_topics = websocket_no_stream(feature_topic_lists, description, all_topic_lists)
    if len(bio) > 2000:
        bio = bio[:2000]
    if len(blog_html) > 20000:
        blog_html = blog_html[:20000]
    # # http的方式
    predict_topics = http_no_stream(bio, blog_html)

    # 输出结果
    print(predict_topics)
