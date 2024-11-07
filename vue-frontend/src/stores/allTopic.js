import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('AllTopic', () => {
    const allTopic = ref([])
    async function getAllTopic() {
        const response = await fetch('/api/get_topic');
    const data = await response.json();
    }
    return { allTopic, getAllTopic }
})