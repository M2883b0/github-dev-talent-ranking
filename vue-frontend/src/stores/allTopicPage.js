import { ref } from 'vue'
import { defineStore } from 'pinia'
export const allTopicPage = defineStore('AllTopic', () => {
    const allTopicPage = ref({})
    async function getAllTopicPage() {
        const response = await fetch('/api/get_topics_page?num=9');
    const data = await response.json();
    allTopicPage.value = data
    }
    return { allTopicPage, getAllTopicPage }
})