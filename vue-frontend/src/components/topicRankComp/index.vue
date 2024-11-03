<template>
    <div class="topic-page">
      <div class="score-title">
        <div class="title">{{ "CompassBench Leaderboard" }}</div>
      </div>
      <div class="rank-items">
          <div class="overall-score"><slot name="s1"/></div>
        <RankItem v-for="(item, index) in rankList" :key="`${item.github_url}-${index}`" :rank="index" :rankInfo="item"/>
      </div>
    </div>
  </template>
  <script setup>
  import RankItem from "./rankItem.vue";
  const props = defineProps({
    rankList:Array
  })
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
    width:100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding:20px 0;
    max-height: 600px;
    overflow-y: auto;
  }
  .overall-score{
      width:95%;
      border-radius: 4px 4px 0 0;
      background: linear-gradient(180deg, #E8F2FF 0%, rgba(232, 242, 255, 0) 100%);
      padding: 8px 16px 12px;
      color: var(--Brand1-6, #1B3882);
      font-size: 16px;
      font-style: normal;
      font-weight: 600;
      line-height: 24px;
  }
  </style>