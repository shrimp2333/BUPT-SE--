<template>
  <el-form :inline="true" :model="formInline" class="demo-form-inline">
    <el-form-item label="用户ID">
      <el-input v-model="formInline.name" placeholder="请输入用户ID"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="onSubmit">查询</el-button>
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
        <el-button type="text" size="small" @click="handleEdit(scope.row)"
          >查看</el-button
        >
        <el-button type="text" size="small" @click="handleClick(scope.row)"
          >修改</el-button
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
      :model="formInline"
      class="demo-form-inline details"
    >
      <el-form-item label="姓名">
        <el-input v-model="details.user_id" placeholder="" disabled></el-input>
      </el-form-item>
      <el-form-item label="内容">
        <el-input
          v-model="details.top_comments_content"
          placeholder=""
          disabled
        ></el-input>
      </el-form-item>
      <el-form-item label="时间">
        <el-input v-model="details.passtime" placeholder="" disabled></el-input>
      </el-form-item>
    </el-form>
    <div style="text-align: center">
      <el-button type="primary" @click="drawer = false">关闭</el-button>
    </div>
  </el-drawer>
  <!--查看弹出框 -->
  <el-dialog v-model="dialogVisible" title="用户信息与充电记录" width="95%">
    <text>用户信息</text>
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
    <text>充电记录</text>
    <el-table :data="logForm">
      <el-table-column prop="detail_id" label="详细id" />
      <el-table-column prop="status" label="状态" />
      <el-table-column prop="generate_time" label="生成时间" />
      <el-table-column prop="charging_pile_id" label="充电桩id" />
      <el-table-column prop="user_id" label="用户id" />
      <el-table-column prop="charging_power" label="充电量" />
      <el-table-column prop="charging_duration" label="充电时间" />
      <el-table-column prop="start_time" label="开始时间" />
      <el-table-column prop="end_time" label="结束时间" />
      <el-table-column prop="charging_fee" label="充电费用" />
      <el-table-column prop="service_fee" label="服务费用" />
      <el-table-column prop="total_fee" label="总费用" />
    </el-table>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, Ref, reactive, toRefs, onMounted } from "vue";
import { ElTable } from "element-plus";
import axios from "axios";

const loading = ref(false); // 是否显示加载效果
const userData: Ref = ref([]); // 用户表格数据
const temuserData: Ref = ref([]); // 临时用户表格数据
const cPage = ref(1);
const drawer = ref(false);
const details: Ref = ref(null);
const form: Ref = ref(null);
const logForm: Ref = ref(null);
const dialogVisible: Ref = ref(null);
const state = reactive({
  formInline: {
    // 搜索数据
    name: "",
  },
  paginObj: {
    // 翻页数据
    currentPage: 1,
    pagesize: 15,
    total: 0,
  },
});

onMounted(() => {
  loading.value = true;
  // 调用接口，获取列表数据
  axios
    .get(
      "http://127.0.0.1:5000/admin/user/list" +
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

// function getDetail(id: string){
//   loading.value = true;
//   axios
//     .get("http://127.0.0.1:5000/admin/user/list"+"?token="+localStorage.getItem("ms_token")+"?id="+id)
//     .then((response) => {
//       console.log("response: ", response.data.data);
//       chargeLog.value = response.data.log;
//       userDetail.value = response.data.user_info;
//       state.paginObj.total = response.data.data.length;
//       loading.value = false;
//     })
// }

// 查询操作
const onSubmit = () => {
  userData.value = temuserData.value.filter(
    // 查询过滤数据
    (item: any) => item.user_id.indexOf(state.formInline.name) >= 0
  );
  current_change(1); // 切换到第一页
  state.paginObj.total = userData.value.length; // 重新设置总数量
};

const handleClick = (row: any) => {
  console.log(row);
  drawer.value = true;
  details.value = row;
};

const handleEdit = (row: any) => {
  loading.value = true;
  axios
    .get(
      "http://127.0.0.1:5000/admin/user/detail" +
        "?token=" +
        localStorage.getItem("ms_token") +
        "?id=" +
        row.user_id
    )
    .then((response) => {
      console.log("response: ", response.data.data);
      console.log("log: ", response.data.data.log);
      console.log("user_info: ", response.data.data.user_info);
      form.value = [response.data.data.user_info];
      logForm.value = response.data.data.log;
      // userDetail.value = response.data.data.user_info;
      // chargeLog.value = response.data.data.log;
      // state.paginObj.total = response.data.data.length;
      loading.value = false;
    })
    .catch((error) => {
      loading.value = false;
      console.error(error);
    });
  // form.value = userDetail.value;
  // logForm.value = chargeLog.value;
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

<template>
	<div class="container">
		<el-tabs v-model="message">
			<el-tab-pane :label="`未读消息(${state.unread.length})`" name="first">
				<el-table :data="state.unread" :show-header="false" style="width: 100%">
					<el-table-column>
						<template #default="scope">
							<span class="message-title">{{ scope.row.title }}</span>
						</template>
					</el-table-column>
					<el-table-column prop="date" width="180"></el-table-column>
					<el-table-column width="120">
						<template #default="scope">
							<el-button size="small" @click="handleRead(scope.$index)">标为已读</el-button>
						</template>
					</el-table-column>
				</el-table>
				<div class="handle-row">
					<el-button type="primary">全部标为已读</el-button>
				</div>
			</el-tab-pane>
			<el-tab-pane :label="`已读消息(${state.read.length})`" name="second">
				<template v-if="message === 'second'">
					<el-table :data="state.read" :show-header="false" style="width: 100%">
						<el-table-column>
							<template #default="scope">
								<span class="message-title">{{ scope.row.title }}</span>
							</template>
						</el-table-column>
						<el-table-column prop="date" width="150"></el-table-column>
						<el-table-column width="120">
							<template #default="scope">
								<el-button type="danger" @click="handleDel(scope.$index)">删除</el-button>
							</template>
						</el-table-column>
					</el-table>
					<div class="handle-row">
						<el-button type="danger">删除全部</el-button>
					</div>
				</template>
			</el-tab-pane>
			<el-tab-pane :label="`回收站(${state.recycle.length})`" name="third">
				<template v-if="message === 'third'">
					<el-table :data="state.recycle" :show-header="false" style="width: 100%">
						<el-table-column>
							<template #default="scope">
								<span class="message-title">{{ scope.row.title }}</span>
							</template>
						</el-table-column>
						<el-table-column prop="date" width="150"></el-table-column>
						<el-table-column width="120">
							<template #default="scope">
								<el-button @click="handleRestore(scope.$index)">还原</el-button>
							</template>
						</el-table-column>
					</el-table>
					<div class="handle-row">
						<el-button type="danger">清空回收站</el-button>
					</div>
				</template>
			</el-tab-pane>
		</el-tabs>
	</div>
</template>

<script setup lang="ts" name="tabs">
import { ref, reactive } from 'vue';

const message = ref('first');
const state = reactive({
	unread: [
		{
			date: '2018-04-19 20:00:00',
			title: '【系统通知】该系统将于今晚凌晨2点到5点进行升级维护'
		},
		{
			date: '2018-04-19 21:00:00',
			title: '今晚12点整发大红包，先到先得'
		}
	],
	read: [
		{
			date: '2018-04-19 20:00:00',
			title: '【系统通知】该系统将于今晚凌晨2点到5点进行升级维护'
		}
	],
	recycle: [
		{
			date: '2018-04-19 20:00:00',
			title: '【系统通知】该系统将于今晚凌晨2点到5点进行升级维护'
		}
	]
});

const handleRead = (index: number) => {
	const item = state.unread.splice(index, 1);
	state.read = item.concat(state.read);
};
const handleDel = (index: number) => {
	const item = state.read.splice(index, 1);
	state.recycle = item.concat(state.recycle);
};
const handleRestore = (index: number) => {
	const item = state.recycle.splice(index, 1);
	state.read = item.concat(state.read);
};
</script>

<style>
.message-title {
	cursor: pointer;
}
.handle-row {
	margin-top: 30px;
}
</style>
