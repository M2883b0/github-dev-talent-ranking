<template>
  <div class="rank-item" @click="goGithub">
    <img :src="getTopImgSrc" v-if="rank <= 2" class="rank-image" />
    <div v-else class="rank">{{ rank + 1 }}</div>
    <el-avatar :size="30" :src="rankInfo.github_url" class="avatar-view">
      <img
        src="https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg"
      />
    </el-avatar>
    <div class="name">{{ rankInfo.name }}</div>
    <div class="name" style="margin-left: 20px" v-if="rankInfo.followers_num">
      粉丝数：{{ rankInfo.followers_num }}
    </div>
    <div class="name" style="margin-left: 20px"  v-if="rankInfo.fork_num">
      fork数：{{ rankInfo.fork_num }}
    </div>
   
    <div class="name" style="margin-left: 20px" v-if="rankInfo.repos_num">
      仓库数：{{ rankInfo.repos_num }}
    </div>
    <div class="name" style="margin-left: 20px" v-if="rankInfo.nation">
      所属国家或地区：{{ rankInfo.nation }}
    </div>
    <div class="name" style="margin-left: 20px" v-if="rankInfo.email_address">
      邮箱：{{ rankInfo.email_address }}
    </div>
    <div
      class="name"
      style="
        margin-left: 20px;
        max-width: 250px;
        white-space: nowrap;
        overflow: hidden; /* 隐藏溢出内容 */
        text-overflow: ellipsis;
      "
      v-if="rankInfo.company"
    >
      公司：{{ rankInfo.company }}
    </div>
    <div
      class="name"
      style="
        margin-left: 20px;
        max-width: 200px;
        white-space: nowrap;
        overflow: hidden; /* 隐藏溢出内容 */
        text-overflow: ellipsis;
      "
      v-if="rankInfo.bio"
    >
      简介：{{ rankInfo.bio }}
    </div>
    <div class="total_talent">综合分数：{{ rankInfo.total_talent }}</div>
  </div>
</template>
<script setup>
import top1 from "@/assets/top1.png";
import top2 from "@/assets/top2.png";
import top3 from "@/assets/top3.png";
import { computed } from "vue";
const topImageList = [top1, top2, top3];
const props = defineProps({
  rank: Number,
  rankInfo: Object,
});
const getTopImgSrc = computed(() => {
  return topImageList[props.rank];
});
const goGithub = () => {
  window.location = props.rankInfo.image_url;
};
</script>
<style scoped>
.rank-item {
  width: 95%;

  height: 60px;
  border-bottom: 1px solid rgb(244, 245, 249);
  display: flex;
  flex-direction: row;
  align-items: center;
  position: relative;
}
.rank-image {
  width: 31px;
  height: 36px;
  margin-left: 10px;
}
.rank {
  margin-left: 10px;
  background-color: rgb(194, 194, 194);
  border-radius: 50%;
  width: 31px;
  height: 31px;
  line-height: 31px;
  text-align: center;
  color: #fff;
  font-size: 16px;
}
.rank-item:hover {
  background-color: rgb(245, 246, 253);
  cursor: pointer;
}
.avatar-view {
  margin: 10px;
}
.name {
  font-size: 16px;
  font-style: normal;
  font-weight: 600;
  line-height: 24px;
}
.total_talent {
  position: absolute;
  right: 20px;
}
</style>