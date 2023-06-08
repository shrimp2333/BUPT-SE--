<template>
  <div>
    <!-- "data_last_day"展示 -->
    <div>
      <el-card class="bigcard">
        <el-row>
          <el-card class="box-card">
            <div>
              <el-text class="mx-1" size="small">昨日总充电量</el-text>
            </div>
            <div>
              <el-text class="mx-1" size="large"
                >{{
                  // ChangeIntToFloat(dataLastDay.total_charging_power)
                  dataLastDay.total_charging_power
                }}度</el-text
              >
            </div>
            <div>
              <el-text class="mx-1" size="small">较前日变化</el-text>
            </div>
            <div>
              <el-text class="mx-1" size="middle">{{
                ChangeDecimalToPercentage(
                  dataLastDay.total_charging_power_change
                )
              }}</el-text>
            </div>
          </el-card>
          <el-card class="box-card">
            <div>
              <el-text class="mx-1" size="small">昨日总充电次数</el-text>
            </div>
            <div>
              <el-text class="mx-1" size="large"
                >{{
                  // ChangeIntToFloat(dataLastDay.total_charging_times)
                  dataLastDay.total_charging_times
                }}次</el-text
              >
            </div>
            <div>
              <el-text class="mx-1" size="small">较前日变化</el-text>
            </div>
            <div>
              <el-text class="mx-1" size="middle">{{
                ChangeDecimalToPercentage(
                  dataLastDay.total_charging_times_change
                )
              }}</el-text>
            </div>
          </el-card>
          <el-card class="box-card">
            <div>
              <el-text class="mx-1" size="small">昨日总充电时间</el-text>
            </div>
            <div>
              <el-text class="mx-1" size="large"
                >{{
                  // ChangeIntToFloat(dataLastDay.total_charging_duration)
                  dataLastDay.total_charging_duration
                }}s</el-text
              >
            </div>
            <div>
              <el-text class="mx-1" size="small">较前日变化</el-text>
            </div>
            <div>
              <el-text class="mx-1" size="middle">{{
                ChangeDecimalToPercentage(
                  dataLastDay.total_charging_duration_change
                )
              }}</el-text>
            </div>
          </el-card>
          <el-card class="box-card">
            <div>
              <el-text class="mx-1" size="small">昨日总收入</el-text>
            </div>
            <div>
              <el-text class="mx-1" size="large"
                >{{
                  // ChangeIntToFloat(dataLastDay.total_fee)
                  dataLastDay.total_fee
                }}元</el-text
              >
            </div>
            <div>
              <el-text class="mx-1" size="small">较前日变化</el-text>
            </div>
            <div>
              <el-text class="mx-1" size="middle">{{
                ChangeDecimalToPercentage(dataLastDay.total_fee_change)
              }}</el-text>
            </div>
          </el-card>
        </el-row></el-card
      >
    </div>
    <!-- "charging_pile_queue"展示 -->
    <div>
      <el-card class="charging_pile_queue">
        <el-text class="mx-1" size="large">充电桩队列</el-text>
        <el-table :data="pileQueue" border style="width: 100%">
          <el-table-column prop="charging_pile_id" label="充电桩id" />
          <el-table-column prop="user_id_list" label="用户队列" />
          <!-- <el-table-column prop="user_id_2" label="用户2" /> -->
        </el-table>
      </el-card>
    </div>
    <!-- "waiting_area_queue"展示 -->
    <div>
      <el-card class="waiting_area_queue">
        <div>
          <el-text class="mx-1" size="large">等候区队列</el-text>
        </div>
        <el-text class="mx-1" size="large">{{ waitQueue }}</el-text>
      </el-card>
    </div>
    <div>
      <el-card class="log">
        <el-text class="mx-1" size="large">充电日志</el-text>
        <el-table :data="logs" border style="width: 100%">
          <el-table-column prop="date" label="日期" />
          <el-table-column prop="total_charging_power" label="总充电量" />
          <el-table-column prop="total_charging_times" label="总充电次数" />
          <el-table-column prop="total_charging_duration" label="总充电时间" />
          <el-table-column prop="charging_fee" label="充电费" />
          <el-table-column prop="service_fee" label="服务费" />
          <el-table-column prop="total_fee" label="总费用" />
        </el-table>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, Ref, reactive, toRefs, onMounted, nextTick } from "vue";
import { ElTable } from "element-plus";
import axios from "axios";
import ChartLine from "./chartLint.vue";
import { getCurrentInstance } from "vue";

const context = getCurrentInstance()?.appContext.config.globalProperties;
const baseUrl = context?.$baseUrl;

// 基于准备好的dom，初始化echarts实例
const loading = ref(false); // 是否显示加载效果
const pileQueue: Ref = ref([]); // 充电桩队列
const waitQueue: Ref = ref([]); // 等候区队列
const logs: Ref = ref([]);
const dataLastDay: Ref = ref({
  total_charging_power: JSON.parse(localStorage.getItem("dataLastDay") + "")
    .total_charging_power,
  total_charging_power_change: JSON.parse(
    localStorage.getItem("dataLastDay") + ""
  ).total_charging_power_change,
  total_charging_times: JSON.parse(localStorage.getItem("dataLastDay") + "")
    .total_charging_times,
  total_charging_times_change: JSON.parse(
    localStorage.getItem("dataLastDay") + ""
  ).total_charging_times_change,
  total_charging_duration: JSON.parse(localStorage.getItem("dataLastDay") + "")
    .total_charging_duration,
  total_charging_duration_change: JSON.parse(
    localStorage.getItem("dataLastDay") + ""
  ).total_charging_duration_change,
  total_fee: JSON.parse(localStorage.getItem("dataLastDay") + "").total_fee,
  total_fee_change: JSON.parse(localStorage.getItem("dataLastDay") + "")
    .total_fee_change,
}); // 昨日数据

onMounted(() => {
  loading.value = true;
  // 调用接口，获取列表数据
  axios
    .get(
      baseUrl +
        "/admin/statistics" +
        "?token=" +
        localStorage.getItem("ms_token")
    )
    .then((response) => {
      console.log("response: ", response.data.data);

      localStorage.setItem(
        "dataLastDay",
        JSON.stringify(response.data.data.data_last_day)
      );
      localStorage.setItem("pileLog", JSON.stringify(response.data.data.log));
      logs.value = response.data.data.log;
      pileQueue.value = response.data.data.charging_pile_queue;
      waitQueue.value = response.data.data.waiting_area_queue;

      loading.value = false;
    })
    .catch((error) => {
      loading.value = false;
      console.error(error);
    });
});

function ChangeDecimalToPercentage(data: any) {
  var data1 = (data * 100).toFixed(2) + "%";
  if (data > 0) return "+" + data1;
  else return data1;
}
function ChangeIntToFloat(data: any) {
  var data1 = data.toFixed(2);
  return data1;
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
.el-card {
  min-width: 380px;
  margin-right: 20px;
  transition: all 0.5s;
}

.box-card{
  width: 20%;
}
</style>
