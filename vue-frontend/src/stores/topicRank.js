import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('topicRank', () => {
  const topicRankList = ref([])
  const topicRankList2 = ref([])
  async function getTopicRank() {
    const response = await fetch('/api/topic_rank');
    const data = await response.json();
    topicRankList.value = data.rank_list 
   }
  async function getTopicRank2(topics) {
    topicRankList2.value = []
    for(let i=0;i<topics.length;i++){
      const response = await fetch(`/api/topic_rank?topic=${topics[i]}`);
      const data = await response.json();
      topicRankList2.value.push(data.rank_list)
    }
  }
  return { topicRankList, getTopicRank,getTopicRank2,topicRankList2 }
})
