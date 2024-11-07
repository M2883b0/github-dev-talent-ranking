import { ref } from 'vue'
import { defineStore } from 'pinia'

export const cxkStore = defineStore('searchUser', () => {
    const searchData = ref({})
    const page = ref(0)
    async function getSearchResult(value) {
        searchData.value = false
        const response = await fetch(`/api/search_users?name=${value}`);
        const data = await response.json();
        searchData.value = data
    }
    return { searchData, getSearchResult }
})