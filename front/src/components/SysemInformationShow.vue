<template>
  <div>
    <el-table border ref="multipleTable" :data="currentPagetableMessage" tooltip-effect="dark" style="width: 100%" @selection-change="handleSelectionChange" height="400" stripe >
    <!--<el-table-column type="selection" width="55"></el-table-column>-->
    <el-table-column align="center" label="id" width="50" :key="Math.random()" :show-overflow-tooltip="true"><template slot-scope="scope">{{ scope.row.id }}</template></el-table-column>
    <el-table-column align="center" prop="ip" label="系统ip" :key="Math.random()" width="130"></el-table-column>
    <el-table-column align="center" prop="username" label="系统账号" :key="Math.random()" width="120"></el-table-column>
    <el-table-column align="center" prop="password" label="系统密码" width="80" :key="Math.random()" v-if='password_show_hide'></el-table-column>
    <el-table-column align="center" prop="ping" label="网络状况" width="120" :key="Math.random()" :show-overflow-tooltip="true"></el-table-column>
    <el-table-column align="center" prop="cpu" label="CPU" width="200":key="Math.random()" :show-overflow-tooltip="true"></el-table-column>
    <el-table-column align="center" prop="memory" label="内存" width="150" :key="Math.random()" :show-overflow-tooltip="true"></el-table-column>
    <el-table-column align="center" prop="disk" label="硬盘空间大小"  width="105" :key="Math.random()"></el-table-column>
    <el-table-column align="center" prop="cpu_rate" label="CPU可用率" width="100" :key="Math.random()"></el-table-column>
    <el-table-column align="center" prop="and32_64" label="查看系统32或64位" width="140" :key="Math.random()"></el-table-column>
    <el-table-column align="center" prop="information" label="查看服务器发行版相关信息" width="200" :key="Math.random()" :show-overflow-tooltip="true"></el-table-column>
    <el-table-column align="center" prop="pci" label="查看PCI设备信息" width="200" :key="Math.random()" :show-overflow-tooltip="true"></el-table-column>
    <!--<el-table-column prop="tableState" label="状态" show-overflow-tooltip></el-table-column>-->
    <el-table-column align="center" label="操作" width="170px":key="Math.random()">
      <template slot-scope="scope">
        <el-button @click.native.prevent="approvalStatus(scope.$index, currentPagetableMessage) " :type="tableStateType" size="mini">{{scope.row.tableState}}</el-button>
        <el-button @click.native.prevent="deleteRow(scope.$index, currentPagetableMessage)" type="danger" size="mini" v-show="button_remove_statu" icon="el-icon-delete">移除</el-button>
      </template>
    </el-table-column>
    </el-table>
    <div style="text-align: center;margin-top: 30px;">
      <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="currentPage" :page-sizes="[5, 10, 20, 40]" :page-size="pagesize" layout="total, sizes, prev, pager, next, jumper" :total="tableMessage.length"></el-pagination></div>
    <el-dialog title="编辑页面" :visible.sync="dialogTableVisible" width="30%" >
      <div><span style="font-size: 10px">OS_IP：</span><el-input style="width: 200px;margin-left:50px" v-model="ip" placeholder="请输入系统ip" size="small"></el-input></div>
      <div style="margin:10px 0"><span style="font-size: 10px">系统登录用户名：</span><el-input style="width: 200px;margin-left:0px" v-model="username" placeholder="请输入用户名" size="small"></el-input>
      </div><div style="margin:10px 0"><span style="font-size: 10px">系统登录密码：</span><el-input style="width: 200px;margin-left:11px" v-model="password" placeholder="请输入密码" size="small" show-password></el-input></div>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialognodecide">取 消</el-button>
        <el-button type="primary" @click="dialogdeicde">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
  import axios from 'axios'
   export default {
//    tableMessage: [{id:'tsest', ip: '192.168.150.8', username: 'Howe',password: '440440440',cpu: '8:00',memory: '10:00',disk:'',cpu_rate:'',and32_64: 'cnsz17',information: '81000',pci: 'CH0022309',ping:'未测试',tableState:'更新'}, ]
//     props:['gettableMessage'],
     data() {return { password_show_hide:false,currentPage:1, pagesize:10,currentPagetableMessage:[],id:"",ip:"",username:"",password:"",dialogTableVisible: false,button_remove_statu:true,tableStateType:'warning',tableMessage: [],multipleSelection: []}},
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
         this.$confirm('此操作将永久删除该信息, 是否继续?', '提示', {confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning'}).then(() => {axios.post(`http://127.0.0.1:5000/update_delete`, {"id":rows[index]["id"]}).then(res => {console.log('res=>', this.$message({message: '系统信息删除成功', type: 'success'}));}).catch(err => {console.log(this.$message.error('系统信息删除失败'))});rows.splice(index, 1);}).catch(() => {this.$message({type: 'info', message: '已取消删除'});});
//        console.log(rows[index]["id"]);

      },approvalStatus(index, rows) {
//         this.tableStateType='info';
//         this.button_remove_statu=false;
//         this.information_first_get();
//         rows[index]["username"]="test"
         this.dialogTableVisible=true
         this.id=rows[index]["id"]
         this.ip=rows[index]["ip"]
         this.username=rows[index]["username"]
         this.password=rows[index]["password"]
      },
       information_first_get: function () {
         axios.get(`http://127.0.0.1:5000/register_get`).then(res=>{console.log(res.data);this.tableMessage=res.data}).catch(err=>{console.log(err)})
         axios.post(`http://127.0.0.1:5000/currentPage_pagesize`,{"currentPage":this.currentPage,"pagesize":this.pagesize}).then(res=>{console.log(res.data);this.currentPagetableMessage=res.data}).catch(err=>{console.log(err)})
       },
       dialogdeicde(){
         let data = {"id":this.id,"ip": this.ip, "username": this.username, "password": this.password,"currentPage":this.currentPage,"pagesize":this.pagesize,};
         axios.post(`http://127.0.0.1:5000/dialogdeicde_update`, data).then(res => {console.log('res=>',this.dialogTableVisible=false,this.currentPagetableMessage=res.data,this.$message({message: '系统信息修改成功', type: 'success'}));}).catch(err => {console.log(this.$message.error('系统信息修改失败'))});
       },
       dialognodecide(){
         this.$message({type: 'info', message: '已取消编辑'});
         this.dialogTableVisible=false
       },
       handleSizeChange: function (size) {
         this.pagesize = size;
         axios.post(`http://127.0.0.1:5000/currentPage_pagesize`,{"currentPage":this.currentPage,"pagesize":this.pagesize}).then(res=>{console.log(res.data);this.currentPagetableMessage=res.data}).catch(err=>{console.log(err)})
//                console.log(this.pagesize)  //每页下拉显示数据
        },
        handleCurrentChange: function(currentPage){
         this.currentPage = currentPage;
         axios.post(`http://127.0.0.1:5000/currentPage_pagesize`,{"currentPage":this.currentPage,"pagesize":this.pagesize}).then(res=>{console.log(res.data);this.currentPagetableMessage=res.data}).catch(err=>{console.log(err)})
//                console.log(this.currentPage)  //点击第几页
        },
     },
    created:function(){
      this.information_first_get()
    }
   }
</script>
