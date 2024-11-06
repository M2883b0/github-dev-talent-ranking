<template>
  <div class="topic-page">
    <div class="score-title">
      <div class="title">{{ "CompassBench Leaderboard" }}</div>
      <el-select
        v-model="国家"
        placeholder="Select"
        style="width: 150px; margin-left: 20px"
      >
        <el-option
          v-for="item in contryList"
          :key="item"
          :label="item"
          :value="item"
        >
          <div class="flex items-center">
            <span>{{ item }}</span>
          </div>
        </el-option>
        <template #tag>
          <div>{{ value }}</div>
        </template>
      </el-select>
    </div>
    <div class="rank-items">
      <div class="overall-score"><slot name="s1" /></div>
      <RankItem
        v-for="(item, index) in rankList"
        :key="`${item.github_url}-${index}`"
        :rank="index"
        :rankInfo="item"
      />
    </div>
  </div>
</template>
  <script setup>
import RankItem from "./rankItem.vue";
import { contryList } from "@/util/data";
import { ref, watch } from "vue";
const props = defineProps({
  rankList: Array,
  index: Number,
});
const 国家 = ref(contryList[0]);
const cxkEmit = defineEmits(["cxk-select"]);
watch(国家, (newValue) => {
  cxkEmit("cxk-select", props.index, newValue);
});
</script>
  <style scoped>
.topic-page {
  width: 80vw;
  min-width: 1000px;
}
.score-title {
  background: linear-gradient(90deg, #1b3882 0%, #5878b4 100%);
  width: 100%;
  height: 80px;
  border-radius: 10px 10px 0 0;
  display: flex;
  flex-direction: row;
  align-items: center;
}
.title {
  margin-left: 30px;
  color: #fff;
}
.rank-items {
  border: 1px solid black;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px 0;
  max-height: 600px;
  overflow-y: auto;
}
.overall-score {
  width: 95%;
  border-radius: 4px 4px 0 0;
  background: linear-gradient(180deg, #e8f2ff 0%, rgba(232, 242, 255, 0) 100%);
  padding: 8px 16px 12px;
  color: var(--Brand1-6, #1b3882);
  font-size: 16px;
  font-style: normal;
  font-weight: 600;
  line-height: 24px;
}
</style>