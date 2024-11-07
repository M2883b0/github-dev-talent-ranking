# dev-github-talent-ranking
根据 GitHub 的开源项目数据，对进行开发者评估和排名。

1、前端，本项目前端需要安装node。前端的配置文件，在`vite.config.js`中，更改后端的服务ip和端口。

```plain
npm run dev
```

导出dist文件的方法, 导出文件放在flask-backend 下template, static文件夹下

```bash
npm run build
```

npm run build

2、后端，本项目使用Flask 后端框架，部署后运行

```bash
python /backend/app.py
```

3、爬虫，使用Scrapy 框架实现，直接运行startSpider.py
```bash
python startSpider.py
```




网站默认首页 [http://127.0.0.1:5173/](http://127.0.0.1:5173/)。

