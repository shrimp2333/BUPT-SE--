<template #default="scope">
  <div>
    <el-form :inline="true" :model="formInline" class="demo-form-inline">
      <el-form-item label="充电桩ID">
        <el-input
          v-model="formInline.name"
          placeholder="请输入充电桩ID"
        ></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">查询</el-button>
      </el-form-item>
      <el-form-item>
        <el-button size="primary" @click="handleChange(0)"
          >修改充电桩状态</el-button
        >
      </el-form-item>
    </el-form>

    <el-table
      stripe
      :data="
        userData.slice(
          (paginObj.currentPage - 1) * paginObj.pagesize,
          paginObj.currentPage * paginObj.pagesize
        )
      "
      style="width: 100%"
      v-loading="loading"
      empty-text="没有数据"
    >
      <el-table-column prop="charging_pile_id" label="充电桩ID" />
      <el-table-column prop="charging_type" label="充电类型" />
      <el-table-column prop="status" label="状态" />
      <el-table-column fixed="right" label="操作">
        <template #default="scope">
          <el-button size="small" @click="handleView(scope.row)"
            >查看详情</el-button
          >
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      background
      v-model:currentPage.sync="cPage"
      layout="prev, pager, next"
      :total="paginObj.total"
      @current-change="current_change"
      style="margin-top: 15px"
    ></el-pagination>
    <!-- 详情页弹出框 -->
    <el-drawer v-model="drawer" title="详情页面">
      <el-form
        :inline="true"
        :model="formDetail"
        class="demo-form-inline details"
      >
        <el-form-item label="充电桩id">
          <el-input v-model="formDetail.id" placeholder=""></el-input>
        </el-form-item>
        <el-form-item label="选择状态">
          <el-select v-model="formDetail.status" placeholder="选择value">
            <el-option label="关闭" value="0" />
            <el-option label="开机" value="1" />
            <el-option label="维修" value="2" />
            <el-option label="电池容量" value="3" />
          </el-select>
        </el-form-item>
      </el-form>
      <div style="text-align: center">
        <el-button
          type="primary"
          @click="
            submit();
            drawer = false;
          "
          >提交</el-button
        >
        <el-button type="primary" @click="drawer = false">关闭</el-button>
      </div>
    </el-drawer>
    <!--查看弹出框 -->
    <el-dialog v-model="dialogVisible" title="充电桩详细信息" width="95%">
      <!-- <text>用户信息</text> -->
      <el-table :data="form">
        <el-table-column prop="charging_pile_id" label="充电桩ID" />
        <el-table-column prop="charging_type" label="充电类型" />
        <el-table-column prop="status" label="状态" />
        <el-table-column prop="charging_fee" label="充电金额" />
        <el-table-column prop="charging_duration" label="充电时长" />
        <el-table-column prop="charging_power" label="充电量" />
      </el-table>
      <!-- <text>充电记录</text> -->
      <el-table :data="logForm">
        <el-table-column prop="charging_pile_id" label="充电桩id" />
        <el-table-column prop="total_charging_times" label="充电次数" />
        <el-table-column prop="total_charging_duration" label="充电时长" />
        <el-table-column prop="date" label="日期" />
        <el-table-column prop="total_charging_power" label="总充电量" />
        <el-table-column prop="charging_fee" label="充电费用" />
        <el-table-column prop="service_fee" label="服务费用" />
        <el-table-column prop="total_fee" label="总费用" />
      </el-table>
      <el-table :data="carForm">
        <el-table-column prop="battery_capacity" label="电池容量" />
        <el-table-column prop="request_power" label="请求充电量" />
        <el-table-column prop="user_id" label="用户id" />
        <el-table-column prop="waiting_time" label="等待时间" />
      </el-table>
      <div style="text-align: center">
        <el-button type="primary" @click="dialogVisible = false"
          >关闭</el-button
        >
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, Ref, reactive, toRefs, onMounted } from "vue";
import { ElTable } from "element-plus";
import axios from "axios";
import { getCurrentInstance } from 'vue'

const context = getCurrentInstance()?.appContext.config.globalProperties;
const baseUrl = context?.$baseUrl;
const loading = ref(false); // 是否显示加载效果
const userData: Ref = ref([]); // 用户表格数据
const temuserData: Ref = ref([]); // 临时用户表格数据
const cPage = ref(1);
const drawer = ref(false);
const details: Ref = ref(null);
const form: Ref = ref(null);
const logForm: Ref = ref(null);
const carForm: Ref = ref(null);
const dialogVisible: Ref = ref(null);
const state = reactive({
  formInline: {
    // 搜索数据
    name: "",
  },
  paginObj: {
    // 翻页数据
    currentPage: 1,
    pagesize: 10,
    total: 0,
  },
});

const formDetail = reactive({
  id: "",
  status: "",
});

onMounted(() => {
  loading.value = true;
  // 调用接口，获取列表数据
  axios
    .get(
      baseUrl +
        "/admin/charge/list" +
        "?token=" +
        localStorage.getItem("ms_token")
    )
    .then((response) => {
      console.log(baseUrl,"response: ", response.data.data);
      userData.value = response.data.data;
      temuserData.value = response.data.data;
      state.paginObj.total = response.data.data.length;
      loading.value = false;
    })
    .catch((error) => {
      loading.value = false;
      console.error(error);
    });
});

// 查询操作
const onSubmit = () => {
  userData.value = temuserData.value.filter(
    // 查询过滤数据
    (item: any) =>
      item.charging_pile_id.toString().indexOf(state.formInline.name) >= 0
  );
  current_change(1); // 切换到第一页
  state.paginObj.total = userData.value.length; // 重新设置总数量
};

const handleChange = (row: any) => {
  drawer.value = true;
};

const submit = () => {
  axios.post(
    baseUrl +
      "/admin/charge/status" +
      "?token=" +
      localStorage.getItem("ms_token") +
      "&id=" +
      formDetail.id +
      "&status=" +
      formDetail.status
  );
  console.log("submit!", formDetail);
};

const handleView = (row: any) => {
  loading.value = true;
  axios
    .get(
      baseUrl +
        "/admin/charge/detail" +
        "?token=" +
        localStorage.getItem("ms_token") +
        "&id=" +
        row.charging_pile_id +
        "&time=" +
        "7"
    )
    .then((response) => {
      console.log("response: ", response.data.data);
      form.value = [response.data.data.charging_pile_info];
      logForm.value = response.data.data.log;
      carForm.value = response.data.data.car_list;
      loading.value = false;
    })
    .catch((error) => {
      loading.value = false;
      console.error(error);
    });
  dialogVisible.value = true;
};

// 点击翻页
const current_change = (currentPage: number) => {
  state.paginObj.currentPage = currentPage;
  cPage.value = currentPage;
};

const { formInline, paginObj } = toRefs(state);
</script>

<style scoped>
.el-table .el-table__cell {
  height: 48px;
  padding: 0;
}
.details .el-form-item {
  width: 100%;
}
</style>
