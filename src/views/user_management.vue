<template>
  <div>
    <el-form :inline="true" :model="formInline" class="demo-form-inline">
      <el-form-item label="用户ID">
        <el-input
          v-model="formInline.name"
          placeholder="请输入用户ID"
        ></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">查询</el-button>
      </el-form-item>
      <el-form-item>
        <el-button size="primary" @click="handleChange(0)"
          >修改用户信息</el-button
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
      <el-table-column prop="user_id" label="用户ID" />
      <el-table-column prop="username" label="用户名" />
      <el-table-column prop="password" label="用户密码" />
      <el-table-column prop="email" label="邮箱" />
      <el-table-column prop="license_plate" label="车牌号" />
      <el-table-column prop="battery_capacity" label="电池容量" />
      <el-table-column prop="car_type" label="车辆类型" />
      <el-table-column prop="created_at" label="创建时间" />
      <el-table-column prop="updated_at" label="更新时间" />
      <el-table-column fixed="right" label="操作">
        <template #default="scope">
          <el-button size="small" @click="handleView(scope.row)"
            >查看详情</el-button
          >
          <el-button size="small" @click="output(scope.row)"
            >导出报表</el-button
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
        :model="userDetail"
        class="demo-form-inline details"
      >
        <el-form-item label="用户id">
          <el-input v-model="userDetail.user_id" placeholder=""></el-input>
        </el-form-item>
        <el-form-item label="value">
          <el-input v-model="userDetail.value" placeholder=""></el-input>
        </el-form-item>
        <el-form-item label="field">
          <el-select v-model="userDetail.field" placeholder="选择value">
            <el-option label="密码" value="0" />
            <el-option label="用户名" value="1" />
            <el-option label="车型" value="2" />
            <el-option label="电池容量" value="3" />
            <el-option label="车牌号" value="4" />
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
    <el-dialog v-model="dialogVisible" title="用户信息与充电记录" width="95%">
      <!-- 用户信息 -->
      <el-table :data="form">
        <el-table-column prop="user_id" label="用户ID" />
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="password" label="用户密码" />
        <el-table-column prop="email" label="邮箱" />
        <el-table-column prop="license_plate" label="车牌号" />
        <el-table-column prop="battery_capacity" label="电池容量" />
        <el-table-column prop="car_type" label="车辆类型" />
        <el-table-column prop="created_at" label="创建时间" />
        <el-table-column prop="updated_at" label="更新时间" />
      </el-table>
      <!-- 充电记录 -->
      <el-table :data="logForm" stripe>
        <el-table-column prop="detail_id" label="详单id" />
        <el-table-column prop="status" label="当前状态" />
        <el-table-column prop="generate_time" label="创建时间">
          <!-- <template slot-scope="scope">
            <span v-if="scope.row.generate_time  != null">
            	{{ parseTime(scope.row.generate_time , "{y}-{m}-{d}") }}
            </span>
          </template> -->
        </el-table-column>
        <el-table-column prop="charging_pile_id" label="充电桩id" />
        <el-table-column prop="charging_type" label="充电类型" />
        <el-table-column prop="user_id" label="用户id" />
        <el-table-column prop="charging_power" label="充电量" />
        <el-table-column prop="charging_duration" label="充电时长" />
        <el-table-column
          prop="start_time"
          label="开始时间"
          :formatter="timeSwap"
        />
        <el-table-column prop="end_time" label="结束时间" />
        <el-table-column prop="charging_fee" label="充电费用" />
        <el-table-column prop="service_fee" label="服务费用" />
        <el-table-column prop="total_fee" label="总费用" />
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
import { getCurrentInstance } from "vue";
import Papa from "papaparse";

const context = getCurrentInstance()?.appContext.config.globalProperties;
const baseUrl = context?.$baseUrl;

const loading = ref(false); // 是否显示加载效果
const userData: Ref = ref([]); // 用户表格数据
const temuserData: Ref = ref([]); // 临时用户表格数据
const cPage = ref(1);
const drawer = ref(false);
const details: Ref = ref(null);
let form: Ref = ref([]);
let logForm: Ref = ref([]);
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

interface UserDetail {
  user_id: string;
  value: string;
  field: string;
}
//修改信息表单
const userDetail = ref<UserDetail>({
  user_id: "",
  value: "",
  field: "",
});

onMounted(() => {
  loading.value = true;
  // 调用接口，获取列表数据
  axios
    .get(
      baseUrl +
        "/admin/user/list" +
        "?token=" +
        localStorage.getItem("ms_token")
    )
    .then((response) => {
      console.log("response: ", response.data.data);
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
    (item: any) => item.user_id.indexOf(state.formInline.name) >= 0
  );
  current_change(1); // 切换到第一页
  state.paginObj.total = userData.value.length; // 重新设置总数量
};

const handleChange = (row: any) => {
  drawer.value = true;
};

//提交修改用户信息请求
const submit = () => {
  const data = new FormData();
  data.append("user_id", userDetail.value.user_id);
  data.append("value", userDetail.value.value);
  data.append("field", userDetail.value.field);

  const resp = fetch(
    baseUrl +
      "/admin/user/modify" +
      "?token=" +
      localStorage.getItem("ms_token"),
    {
      method: "POST",
      body: data,
    }
  ).then(async (res) => JSON.parse(await res.text()));
  console.log(resp);

  console.log("submit!");
};

//获取详细信息
const handleView = (row: any) => {
  loading.value = true;
  axios
    .get(
      baseUrl +
        "/admin/user/detail" +
        "?token=" +
        localStorage.getItem("ms_token") +
        "&id=" +
        row.user_id
    )
    .then((response) => {
      console.log("response: ", response.data.data);
      form.value = [response.data.data.user_info];
      logForm.value = response.data.data.log;
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

const output = (row: any) => {
  loading.value = true;
  axios
    .get(
      baseUrl +
        "/admin/user/detail" +
        "?token=" +
        localStorage.getItem("ms_token") +
        "&id=" +
        row.user_id
    )
    .then((response) => {
      console.log("responseout: ", response.data.data);

      const columns_title = [
        "班级号_组号_车辆号",
        "充电量",
        "充电类型",
        "充电时间",
        "费用",
      ];
      // 创建一个新的数组，用于存储按指定顺序重排的数据
      const reorderedData = [];

      // 遍历原始表格数据
      for (let i = 0; i < response.data.data.log.length; i++) {
        const newRow = [];
        // 根据指定的列名顺序，依次将对应的值添加到新的行中
        newRow.push(response.data.data.user_info.user_id);
        newRow.push(response.data.data.log[i].charging_power);
        if (response.data.data.log[i].charging_type === 0) {
          newRow.push("慢充");
        } else if (response.data.data.log[i].charging_type === 1) {
          newRow.push("快充");
        }

        const endTime = new Date(response.data.data.log[i].end_time);
        const endHours = endTime.getHours().toString().padStart(2, "0");
        const endMinutes = endTime.getMinutes().toString().padStart(2, "0");
        const endSeconds = endTime.getSeconds().toString().padStart(2, "0");
        const endTimeFormatted = `${endHours}:${endMinutes}:${endSeconds}`;

        // 转换开始时间
        const startTime = new Date(response.data.data.log[i].start_time);
        const startHours = startTime.getHours().toString().padStart(2, "0");
        const startMinutes = startTime.getMinutes().toString().padStart(2, "0");
        const startSeconds = startTime.getSeconds().toString().padStart(2, "0");
        const startTimeFormatted = `${startHours}:${startMinutes}:${startSeconds}`;

        newRow.push(startTimeFormatted + "-" + endTimeFormatted);
        newRow.push(response.data.data.log[i].total_fee);
        // 将新的行添加到重排后的数据数组中
        reorderedData.push(newRow);
      }

      // 生成CSV数据
      const csvData = Papa.unparse({
        fields: columns_title,
        data: reorderedData,
      });

      // 将字符串转换为UTF-8编码
      const encoder = new TextEncoder();
      const csvDataEncoded = encoder.encode(csvData);

      // 创建Blob对象
      const blob = new Blob([csvDataEncoded], { type: "text/csv" });

      // 创建下载链接
      const downloadLink = document.createElement("a");
      downloadLink.href = URL.createObjectURL(blob);
      downloadLink.download = "output.csv";

      // 模拟点击下载链接
      downloadLink.click();

      // 释放URL对象
      URL.revokeObjectURL(downloadLink.href);
      loading.value = false;
    })
    .catch((error) => {
      loading.value = false;
      console.error(error);
    });
};

function timeSwap(row: any) {
  const startTime = new Date(row.start_time);
  const startYears = startTime.getFullYear().toString();
  const startMonth = startTime.getMonth().toString();
  const startDays = startTime.getDate().toString();
  const startHours = startTime.getHours().toString().padStart(2, "0");
  const startMinutes = startTime.getMinutes().toString().padStart(2, "0");
  const startSeconds = startTime.getSeconds().toString().padStart(2, "0");
  const startTimeFormatted = `${startYears}-${startMonth}-${startDays} ${startHours}:${startMinutes}:${startSeconds}`;
  return startTimeFormatted;
}
</script>

<style scoped>
.el-table .el-table__cell {
  height: 48px;
  padding: 0;
}
.details .el-form-item {
  width: 100%;
}

.output {
  position: fixed;
  width: 80px;
  height: 40px;
  bottom: 150px;
  right: 20px;
  text-align: center;
  font-size: 14px;
  z-index: 999;
}
</style>
