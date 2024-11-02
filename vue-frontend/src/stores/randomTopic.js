import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('randomTopic', () => {
    const randomTopicList = ref([])
    async function getRandomTopicList() {
        // const response = await fetch('http://127.0.0.1:4523/m2/5377779-5050372-default/228559871');
        // const data = await response.json();
        randomTopicList.value = [
            {
                "tpoic_name": "abap2UI5",
                "topic_url": "https://github.com/topic/abap2UI5",
                "topic_img_url": "https://raw.githubusercontent.com/github/explore/54ab64c16bdf4604d4fbb36326be6909d8088dcb/topics/abap2ui5/abap2ui5.png",
                "descrip": "abap2UI5 is a framework for developing UI5 apps purely in ABAP — no need for JavaScript, OData, or RAP! It is designed for both cloud and on-premise environments, offering a lightweight and easy-to-install solution that works across all ABAP systems, from NetWeaver 7.02 to ABAP Cloud.",
                "repos_num": 26,
                "is_feature": 0
            },
            {
                "tpoic_name": "Actions",
                "topic_url": "https://github.com/topic/Actions",
                "topic_img_url": "https://raw.githubusercontent.com/github/explore/2c7e603b797535e5ad8b4beb575ab3b7354666e1/topics/actions/actions.png",
                "descrip": "b.com/toolmantim/release-drafter)### Getting Started- [Hello GitHub Actions](https://lab.github.com/github/hello-github-actions!)- [GitHub Actions: Continuous Delivery](https://lab.github.com/githubtraining/github-actions:-continuous-delivery)- [JavaScript](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/creating-a-javascript-action)- [Ruby](https://dev.to/mscccc/build-a-github-action-with-ruby-3nln)- [Rust](https://svartalf.info/posts/2019-09-16-github-actions-for-rust/)#### Community & Support- [Help Documentation](https://help.github.com/en/github/automating-your-workflow-with-github-actions/about-github-actions)- [GitHub Actions Community Forum](https://github.community/t5/GitHub-Actions/bd-p/actions)**Taking Action With GitHub Actions**[//youtube-embed-unfurl//]: # (GVpIaEoFF3A)",
                "repos_num": 5185,
                "is_feature": 1
            },
            {
                "tpoic_name": "adventure-game",
                "topic_url": "https://github.com/topic/adventure-game",
                "topic_img_url": "",
                "descrip": "A video game in which the player assumes the role of a protagonist in an interactive story driven by exploration and puzzle-solving",
                "repos_num": 412,
                "is_feature": 0
            },
            {
                "tpoic_name": "python",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1
            },
            {
                "tpoic_name": "python",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1
            }
        ]
    }
    return { randomTopicList, getRandomTopicList }
})