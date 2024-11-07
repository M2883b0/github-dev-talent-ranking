<template>
      <el-input

    v-model="input"
    style="width: 600px;margin:100px 0 100px 800px;"
    placeholder="请输入要搜索的具体领域"
    class="input-with-select"
    size="large"
      @keyup.enter="handleSearch"
  >
    <template #prepend>
      <el-button :icon="Search" @click="handleSearch" />
    </template>
  </el-input>
    <el-row >
        <el-col :span="3" style="margin-left: 500px;">
        <div style="height: 1000px; overflow-y: auto">
          <el-anchor
            :container="containerRef"
            direction="vertical"
            type="default"
            @click="handleClick"
            :offset="0"
          >
            <template :span="18" v-for="(item, index) in store.allTopicPage">
              <el-anchor-link :href="`#part${index}`" :title="index" />
              <el-anchor-link
                v-for="cxkitem in item"
                :title="cxkitem.name"
                :href="`#part${cxkitem.name}-child`"
              ></el-anchor-link>
            </template>
          </el-anchor>
        </div>
      </el-col>

      <el-col :span="9">
        <div ref="containerRef" style="height: 1000px; overflow-y: auto">
          <div v-for="(item, index) in store.allTopicPage" class="topic-list">
            <div :id="`part${index}`" ></div>
            <TopicItem v-for="cxkitem in item" :id="`part${cxkitem.name}-child`" :topicInfo="cxkitem" />
            <!-- <div :id="`part${cxkitem.name}`" v-for="cxkitem in item">
              {{ cxkitem.name }}
            </div> -->
          </div>
        </div>
      </el-col>
     
    </el-row>
</template>
  
<script setup>
import { allTopicPage } from "@/stores/allTopicPage.js";
import { onMounted, ref,watch } from "vue";
import TopicItem from "../topicItem/topicItem.vue";
import router from "@/router/index.js";
import { cxkStore2 } from "@/stores/cxksearchtopic.js";
const store2 = cxkStore2();
const store = allTopicPage();
const containerRef = ref(null);

const handleClick = (e) => {
  e.preventDefault();
};
onMounted(() => {
  store.getAllTopicPage();
});
const input = ref("")
const handleSearch = ()=>{
  store2.getSearchResult( input.value);
}
watch(  
  () => store2.searchData, // 要观察的数据源，这里是一个 getter 函数  
  (newData, oldData) => { // 当数据源变化时执行的回调函数  

      store2.RelateTopic(store2.searchname);
      store2.TopicRank(store2.searchname)
      router.push({ name: "cxkcxkcxkcxk" });  

  },  
);  
</script>
<style scoped>

.topic-list {
  width: 800px;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
 
}
</style>