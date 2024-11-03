import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('randomTopic', () => {
    const randomTopicList = ref([])
    async function getRandomTopicList() {
        const response = await fetch('/api/random_topic');
        const data = await response.json();
        randomTopicList.value = data.topic_list
    }
    return { randomTopicList, getRandomTopicList }
})