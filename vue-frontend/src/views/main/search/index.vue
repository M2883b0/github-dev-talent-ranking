<template>
  <el-input
    v-model="input"
    style="width: 600px"
    placeholder="请输入要搜索的领域或用户"
    class="input-with-select"
    size="large"
    @keyup.enter="handleSearch"
  >
    <template #prepend>
      <el-button :icon="Search" @click="handleSearch" />
    </template>
    <template #append>
      <el-select
        v-model="select"
        placeholder="选择"
        style="width: 115px; height: 40px"
      >
        <el-option label="领域" :value="1" />
        <el-option label="用户" :value="2" />
      </el-select>
    </template>
  </el-input>
</template>
<script setup>
import { Search } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";
import { ref, watch,computed } from "vue";
import { cxkStore } from "@/stores/searchUser.js";
import { cxkStore2 } from "@/stores/searchTopic.js";
import router from "@/router/index.js";
const store = cxkStore();
const store2 = cxkStore2();
const input = ref("");
const select = ref("");
const handleSearch = () => {
  console.log("搜索内容:", input.value, "选择:", select.value);
  if (select.value === "") {
    ElMessage({
      message: "请选择要搜索的领域或者用户",
      type: "warning",
    });
    return;
  }
  if (input.value === "") {
    ElMessage({
      message: "请输入内容",
      type: "warning",
    });
    return;
  }
  if(select.value === 2){
    store.getSearchResult( input.value);
  }
  else{
    store2.getSearchResult( input.value);
  }
 
};
const routeName = computed(() => {  
  return select.value === 1 ? "searchTopic" : "searchUser";  
});  
watch(  
  () => store.searchData, // 要观察的数据源，这里是一个 getter 函数  
  (newData, oldData) => { // 当数据源变化时执行的回调函数  
    console.log(routeName.value)
      router.push({ name: routeName.value });  
  },  
);  
watch(  
  () => store2.searchData, // 要观察的数据源，这里是一个 getter 函数  
  (newData, oldData) => { // 当数据源变化时执行的回调函数  
    console.log(routeName.value)
      router.push({ name: routeName.value });  
  },  
);  
</script>
<style scoped>
::v-deep .el-select__wrapper {
  height: 40px;
}
</style>