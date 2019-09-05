<template>
  <div style="text-align: center">
   <el-card shadow="hover" style="font-size: 30px;color: #3A7734">Linux多个系统信息自动获取平台</el-card>
   <el-card shadow="hover" ><register @Register_Button="getRegister"/></el-card>
   <el-card shadow="hover" ><search @Search_Button="getSearch" @Select_Password_Button="get_Select_Password"/></el-card>
   <el-card shadow="hover"><sysem-information-show ref="messagesTableRef"/></el-card>
  <!--<foot style="position: absolute;bottom: 0;left: 50%;transform: translate(-50%, -50%);"/>-->

  <foot/>
  </div>
</template>


<script>

  import Register from './Register.vue'
  import SysemInformationShow from './SysemInformationShow.vue'
  import Foot from './Footer.vue'
  import Search from './search.vue'

  export default{
    data (){
      return{

      }
    },
    methods:{
      getRegister(msg){
        console.log(msg);
//        console.log(this.$refs.messagesTableRef.tableMessage);
        console.log(this.$refs.messagesTableRef.information_first_get());
        this.$refs.messagesTableRef.information_first_get();
      },
      getSearch(msg){
//          console.log(this.$refs.messagesTableRef.currentPagetableMessage);
//        console.log(msg[0]["tableState"]);
        if (msg[0]["tableState"]=="此信息已删除")
            this.$refs.messagesTableRef.button_remove_statu=false;
        this.$refs.messagesTableRef.currentPagetableMessage=msg;
      },
      get_Select_Password(msg){
          this.$refs.messagesTableRef.password_show_hide=msg;
          console.log(msg);
      }
    },
    components:{
      Register,
      Search,
      Foot,
      SysemInformationShow
    }
  }
</script>
