<template>
  <div class="topic-item" @click="goGithub">
    <el-image :src="topicInfo.topic_img_url" class="imagecxk">
      <template #error>
        <img
          src="https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg"
          style="width: 100%; height: 100%"
        />
      </template>
    </el-image>
    <div>{{ topicInfo.tpoic_name }}</div>
    <div class="cxknum">repos数量：{{ topicInfo.repos_num }}</div>
    <div v-if="topicInfo.is_feature" class="cxkjx">精选</div>
  </div>
</template>
<script setup>
const props = defineProps({
  topicInfo: Object,
});
const goGithub = () => {
  window.location = props.topicInfo.topic_url;
};
</script>
<style scoped>
.topic-item {
  height: 200px;
  width: 200px;
  transition: box-shadow 0.3s ease; /* 平滑过渡效果 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 初始状态下较小的阴影 */
  overflow: hidden;
  margin: 10px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  position: relative;
  align-items: center;
  padding: 20px;
}
.imagecxk {
  margin-top: 10px;
  width: 50px;
  height: 50px;
}
.topic-item:hover {
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2); /* 鼠标悬停时增加阴影大小和模糊度 */
}
.cxknum {
  position: absolute;
  bottom: 50px;
  left: 20px;
}
.cxkjx {
  position: absolute;
  top: 0px;
  right: 0px;
  font-size: 15px;
  height: 28px;
  padding: 0 11px;
  background-color: #e85a29;
  border-radius: 0px 0px 0px 16px;
  color: #fff;
}
</style>