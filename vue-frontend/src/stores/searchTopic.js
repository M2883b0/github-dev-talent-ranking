import { ref } from 'vue'
import { defineStore } from 'pinia'

export const cxkStore2 = defineStore('searchTopic', () => {
    const searchData = ref({})
    const page = ref(0)
    async function getSearchResult(value) {
        const response = await fetch(`/api/get_topic?topic=${value}&is_letter=false`);
        const data = await response.json();                                                               
        searchData.value = data
    }
    return { searchData, getSearchResult }
})