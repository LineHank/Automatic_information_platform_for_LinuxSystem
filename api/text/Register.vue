<!--import ElementUI from 'element-ui'-->
<!--import 'element-ui/lib/theme-chalk/index.css'-->
<!--Vue.use(ElementUI)-->
<!--import Index from './components/index'-->

<template>
  <div style="text-align: center">
    <div>
      <span style="font-size: 10px">OS_IP：</span>
      <el-input style="width: 200px;margin-left:50px" v-model="ip" placeholder="请输入系统ip" size="small"></el-input>
    </div>
    <div style="margin:10px 0">
      <span style="font-size: 10px">系统登录用户名：</span>
      <el-input style="width: 200px;margin-left:0px" v-model="username" placeholder="请输入用户名" size="small"></el-input>
    </div>
    <div style="margin:10px 0">
      <span style="font-size: 10px">系统登录密码：</span>
      <el-input style="width: 200px;margin-left:11px" v-model="password" placeholder="请输入密码" size="small"></el-input>
    </div>
    <el-button style="width: 130px" type="primary" >上传<i class="el-icon-upload el-icon--right"></i>
    </el-button>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        ip: '',
        username: '',
        password: '',
      }
    },
    methods: {
      register: function () {
        let that = this;
        that.$http.post('http://127.0.0.1:5000/register', {
          ip: that.ip,
          username: that.username,
          password: that.password
        }).then(function (response) {
          console.log(response.data)
          if (parseInt(response.data.code) === 200) {
//            that.$router.push('login')
          }
        }).catch(function (error) {
          console.log(error)
        })
      }
    }
  }
</script>
