import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('topicRank', () => {
  const topicRankList = ref([])
  async function getTopicRank() {
    const response = await fetch('http://127.0.0.1:4523/m2/5377779-5050372-default/228559871');
    const data = await response.json();
    
    topicRankList.value = [
      {
        "login_name": "GreemDev",
        "name": "Evan Husted",
        "github_url": "https://github.com/GreemDev",
        "image_url": "https://avatars.githubusercontent.com/u/28578990?v=4github_url",
        "email": "greem@greemdev.net",
        "bio": "Lead Developer of the Discord bot Volte and my common library Gommon.",
        "company": "@Polyhaze",
        "nation": "中国",
        "repos_num": 20,
        "stars_num": 253,
        "followers_num": 149,
        "fork_num": 12,
        "have_topic": [
          "C#",
          "java"
        ],
        "have_topic_talent": [
          100,
          10
        ],
        "total_talent": 150
      },
      {
        "login_name": "alanalanlu",
        "name": "",
        "github_url": "https://github.com/alanalanlu",
        "image_url": "https://avatars.githubusercontent.com/u/46388471?v=4",
        "email": "",
        "bio": "",
        "company": "",
        "nation": "美国",
        "repos_num": 20,
        "stars_num": 7,
        "followers_num": 30,
        "fork_num": 2,
        "have_topic": [
          "Python",
          "JavaScript",
          "Jupyter Notebook",
          "CSS"
        ],
        "have_topic_talent": [
          100,
          110,
          120,
          50
        ],
        "total_talent": 100
      },
      {
        "login_name": "zhangsan",
        "name": "zhang",
        "github_url": "github_url",
        "image_url": "xxx/png",
        "email": "xxxxx@xx.com",
        "bio": "I am a dog xxxx.",
        "company": "Google Inc",
        "nation": "China",
        "repos_num": 7,
        "stars_num": 41341,
        "followers_num": 394,
        "fork_num": 32131,
        "have_topic": [
          "Linux",
          "C",
          "C++"
        ],
        "have_topic_talent": [
          100,
          110,
          120
        ],
        "total_talent": 330
      },
      {
        "login_name": "zhangsan",
        "name": "zhang",
        "github_url": "github_url",
        "image_url": "xxx/png",
        "email": "xxxxx@xx.com",
        "bio": "I am a dog xxxx.",
        "company": "Google Inc",
        "nation": "China",
        "repos_num": 7,
        "stars_num": 41341,
        "followers_num": 394,
        "fork_num": 32131,
        "have_topic": [
          "Linux",
          "C",
          "C++"
        ],
        "have_topic_talent": [
          100,
          110,
          120
        ],
        "total_talent": 330
      },
      {
        "login_name": "zhangsan",
        "name": "zhang",
        "github_url": "github_url",
        "image_url": "xxx/png",
        "email": "xxxxx@xx.com",
        "bio": "I am a dog xxxx.",
        "company": "Google Inc",
        "nation": "China",
        "repos_num": 7,
        "stars_num": 41341,
        "followers_num": 394,
        "fork_num": 32131,
        "have_topic": [
          "Linux",
          "C",
          "C++"
        ],
        "have_topic_talent": [
          100,
          110,
          120
        ],
        "total_talent": 330
      }
    ]
  }
  return { topicRankList, getTopicRank }
})
