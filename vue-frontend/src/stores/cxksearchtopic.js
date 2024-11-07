import { ref } from 'vue'
import { defineStore } from 'pinia'

export const cxkStore2 = defineStore('cxksearchtopic', () => {
    const searchData = ref({})
    const searchname = ref('')
    const relateTopicList = ref([])
    const topicRankList = ref([]) //不分领域
    async function getSearchResult(value) {
        const response = await fetch(`/api/get_topic?topic=${value}&is_letter=true`);
        const data = await response.json();
        searchData.value = data
     
        searchname.value = data.topic_list[0].name
        console.log("data",searchname.value)
    }
    async function RelateTopic(name) {
        const response = await fetch(`/api/relate_topic?topic=${name}&num=6`);
        relateTopicList.value = []
        const data = await response.json();
        relateTopicList.value = data.relate_topic_list || data.topic_list
        console.log(relateTopicList.value)
    }
    async function TopicRank(name, nation = null) {
        topicRankList.value = []
        let response2
        if (nation === null) {
            response2 = await fetch(`/api/topic_rank?topic=${name}`);
        }
        else {
            response2 = await fetch(`/api/topic_rank?topic=${name}&nation=${nation}`);
        }
        const data2 = await response2.json();
        topicRankList.value = data2.rank_list

    }
    // topic
    return { searchData, getSearchResult, relateTopicList, TopicRank, topicRankList, searchname,RelateTopic }
})