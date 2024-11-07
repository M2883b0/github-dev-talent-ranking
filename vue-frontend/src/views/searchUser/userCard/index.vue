<template>
  <div class="cardcxk">
    <el-avatar :size="60" :src="userInfo.github_url" class="cxk-avatar-view" @click="goGithub">
      <img
        src="https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg"
      />
    </el-avatar>
    <div class="cxk-name">{{ userInfo.name }}</div>
    <div class="cxk-email">{{ userInfo.email }}</div>
    <div style="margin: 10px 0;">综合评分：{{ userInfo.total_talent }}</div>
    <div class="cxk-card-num">
      <div v-for="(item, index) in cardList" :key="index">{{item[1]}}
        <div class="cxk-nums">{{ item[2]??'暂无数据' }}</div>
        
      </div>
    </div>
    
    <div class="allcxk">
      <div v-for='(item,index) in userInfo.have_topic' class="allcxk2">
        <div>所属领域:{{ item }}</div>
        <div>分数:{{userInfo.have_topic[index]  }}</div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { computed } from "vue";

const cxkProps = defineProps({
  userInfo: Object,
});
const cardList = computed(() => {
  return [
    { 1: "仓库数", 2: cxkProps.userInfo.repos_num },
    { 1: "点赞数", 2: cxkProps.userInfo.stars_num },
    { 1: "分数", 2: cxkProps.userInfo.followers_num },
    { 1: "fork数", 2: cxkProps.userInfo.fork_num },
  ];
});
const goGithub = ()=>{
    window.location = cxkProps.userInfo.image_url
}
</script>
<style scoped>
.cardcxk {
  width: 300px;
  height: 400px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  align-self: flex-start;
  margin-left: 200px;
  padding: 20px;
  border-radius: 10px;
  position: relative;
}
.cxk-name {
  position: absolute;
  left: 90px;
  top: 25px;
  font-size: 20px;
  font-weight: 600;
}
.cxk-avatar-view:hover{
    cursor: pointer;
}
.cxk-avatar-view {
  width: 60px;
  height: 60px;
}
.cxk-email {
  position: absolute;
  left: 90px;
  top: 50px;
}

.cxk-card-num{
    position: absolute;
    top:130px;
    left:0;
    width:100%;
    display: flex;
    justify-content: space-around;
    font-size: 18px;
    font-weight: 800;
}
.cxk-nums{
    text-align: center;
    font-size: 16px;
    color:rgba(0, 0, 0, 0.6);
    font-weight: 600;
}
.allcxk{
  position: absolute;
  top:160px;
  left:0;    width:100%;
  height:230px;
  overflow-y: auto;
}
.allcxk2{
  height:30px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  padding: 0 10px;
}
</style>