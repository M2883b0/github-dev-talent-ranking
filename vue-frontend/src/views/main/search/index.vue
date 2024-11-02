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
import { ElMessage } from 'element-plus'
import { ref } from "vue";
const input = ref("");
const select = ref("");
const handleSearch = () => {
  console.log("搜索内容:", input.value, "选择:", select.value);
  if (select.value === "") {
    ElMessage({
      message: "请选择要搜索的领域或者用户",
      type: "warning",
    });
  }
};
</script>
<style scoped>
::v-deep .el-select__wrapper {
  height: 40px;
}
</style>