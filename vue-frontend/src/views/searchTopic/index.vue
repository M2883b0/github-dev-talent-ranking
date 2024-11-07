
<script setup>
import AllTopicPage from '@/components/alltopicpage/index.vue'
import { cxkStore2 } from "@/stores/searchTopic.js";
const store = cxkStore2();
import { onMounted, ref } from "vue";
import TopicItem from "@/components/topicItem/topicItem.vue";
const containerRef = ref(null);

const handleClick = (e) => {
  e.preventDefault();
};
</script>

<template>

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
            <template :span="18" v-for="(item, index) in store.searchData.topic_list">
              <el-anchor-link :href="`#part${index}`" :title="item.name" />
            </template>
          </el-anchor>
        </div>
      </el-col>

      <el-col :span="9">
        <div ref="containerRef" style="height: 1000px; overflow-y: auto"  class="topic-listss">
          <div v-for="(item, index) in store.searchData.topic_list">
            <TopicItem  :topicInfo="item" :id="`part${index}`"/>
          </div>
        </div>
      </el-col>
     
    </el-row>
</template>

<style scoped>

.topic-listss {
  width: 800px;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
}
</style>
  
