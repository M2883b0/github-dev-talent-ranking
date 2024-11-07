import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('topicRank', () => {
  const topicRankList = ref([]) //不分领域
  const topicRankList2 = ref([]) //细分的几个领域
  async function getTopicRank(nation = null) {
    let response
    if (nation == '所有'||nation == null) {
      response = await fetch(`/api/topic_rank`);
    }
    else{
      response = await fetch(`/api/topic_rank?nation=${nation}`);
    }
    const data = await response.json();
    topicRankList.value = data.rank_list
  }
  async function getTopicRank2(topics, nation = null, index) {
    if (typeof topics !== "string") {
      topicRankList2.value = []
      for (let i = 0; i < topics.length; i++) {
        let response
        if(nation==null){
          response = await fetch(`/api/topic_rank?topic=${topics[i]}`);
        }
        else{
          response = await fetch(`/api/topic_rank?topic=${topics[i]}&nation=${nation}`);
        }
        const data = await response.json();
        topicRankList2.value.push(data.rank_list)
      }
      return
    }
    let response
    if (nation == '所有'||nation == null||nation==undefined) {
      response = await fetch(`/api/topic_rank?topic=${topics}`);
    }
    else{
      response = await fetch(`/api/topic_rank?topic=${topics}&nation=${nation}`);
    }
    const data = await response.json();
    topicRankList2.value[index] = data.rank_list
  }
  return { topicRankList, getTopicRank, getTopicRank2, topicRankList2 }
}) 
