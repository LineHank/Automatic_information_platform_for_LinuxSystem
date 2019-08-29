<template>
  <div>
    <el-table border ref="multipleTable" :data="tableMessage" tooltip-effect="dark" style="width: 100%" @selection-change="handleSelectionChange" height="500">
    <el-table-column type="selection" width="55"></el-table-column>
    <el-table-column fixed="left"label="id" width="50"show-overflow-tooltip><template slot-scope="scope">{{ scope.row.id }}</template></el-table-column>
    <el-table-column fixed="left" prop="ip" label="系统ip" width="120"></el-table-column>
    <el-table-column prop="username" label="系统账号" width="120"></el-table-column>
    <el-table-column prop="password" label="系统密码" width="120"></el-table-column>
    <el-table-column prop="cpu" label="CPU" width="200" show-overflow-tooltip></el-table-column>
    <el-table-column prop="memory" label="内存" width="150" show-overflow-tooltip></el-table-column>
    <el-table-column prop="disk" label="硬盘空间大小" width="105"></el-table-column>
    <el-table-column prop="cpu_rate" label="CPU可用率" width="100"></el-table-column>
    <el-table-column prop="and32_64" label="查看系统32或64位" width="140"></el-table-column>
    <el-table-column prop="information" label="查看服务器发行版相关信息" width="200" show-overflow-tooltip></el-table-column>
    <el-table-column prop="pci" label="查看PCI设备信息" width="200" show-overflow-tooltip></el-table-column>
    <el-table-column prop="tableState" label="状态" show-overflow-tooltip></el-table-column>
    <el-table-column fixed="right" label="操作" width="170px">
      <template slot-scope="scope">
        <el-button @click.native.prevent="approvalStatus(scope.$index, tableMessage) " :type="tableStateType" size="mini">{{scope.row.tableState}}</el-button>
        <el-button @click.native.prevent="deleteRow(scope.$index, tableMessage)" type="danger" size="mini" v-show="button_remove_statu" icon="el-icon-delete">移除</el-button>
      </template>
    </el-table-column>
    </el-table>

    <div style="text-align: center;margin-top: 30px;"><el-pagination background layout="prev, pager, next" :total="total" @current-change="current_change"></el-pagination></div>
  </div>
</template>

<script>
  import axios from 'axios'
   export default {
//     props:['gettableMessage'],
     data() {return {button_remove_statu:true,tableStateType:'warning',tableMessage: [{id:'tsest', ip: '192.168.150.8', username: 'Howe',password: '440440440',cpu: '8:00',memory: '10:00',disk:'',cpu_rate:'',and32_64: 'cnsz17',information: '81000',pci: 'CH0022309',tableState:'更新'}, ],multipleSelection: []}},
     methods: {
       toggleSelection(rows) {
        if (rows) {
           rows.forEach(row => {
             this.$refs.multipleTable.toggleRowSelection(row);
           });
         } else {
          this.$refs.multipleTable.clearSelection();
         }
      },
      handleSelectionChange(val) {
        this.multipleSelection = val;
      },deleteRow(index, rows) {
        rows.splice(index, 1);
      },approvalStatus(index, rows) {
         this.tableStateType='info';
         this.button_remove_statu=false;
         this.information_first_get();
      },
       information_first_get: function () {
         axios.get(`http://127.0.0.1:5000/register_get`).then(res=>{console.log(res.data);this.tableMessage=res.data}).catch(err=>{console.log(err)})
       }
     },
    created:function(){
      this.information_first_get()
    }
   }
</script>
