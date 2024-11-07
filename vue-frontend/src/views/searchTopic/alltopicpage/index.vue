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
import { onMounted, ref } from "vue";
import TopicItem from "../../../components/topicitem/topicItem.vue";
const store = allTopicPage();
const containerRef = ref(null);

const handleClick = (e) => {
  e.preventDefault();
};
onMounted(() => {
  store.getAllTopicPage();
});
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