<template>
   <div>
     <span><el-switch v-model="select_password" active-text="显示密码" inactive-text="隐藏密码" @change="Select_Password"></el-switch> &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;&nbsp; </span>
     <span style="font-size: 3px">IP:</span>
     <el-autocomplete style="width: 180px;height:1px;font-size: 3px" v-model="ip_state" :fetch-suggestions="Ip_querySearch" placeholder="输入搜索IP" @select="IP_handleSelect" clearable >
       <template slot-scope="{ item }">
         <div class="ip">{{ item.value }}</div>
         <span class="id">id:{{ item.id }}</span>
         <span class="username">&nbsp;用户名:{{ item.username }}</span>
        </template>
     </el-autocomplete>
     <el-button type="primary" icon="el-icon-search" @click="get_search_message">搜索</el-button>
   </div>
</template>


<<script>
  import axios from 'axios'
   export default{
     data(){return{select_password: false, messages:[],ip_state:'', id_state:'',  IP_restaurants:[],    }
       },
     methods: {
         Ip_querySearch(queryString, cb) {
        for(var i=0;i<this.IP_restaurants.length;i++){
          this.IP_restaurants[i].value = this.IP_restaurants[i].ip
        }
        var restaurants = this.IP_restaurants;
        var results = queryString ? restaurants.filter(this.createFilter(queryString)) : restaurants;
        // 调用 callback 返回建议列表的数据
        cb(results);
      },    //获取ip api数据
       createFilter(queryString) {
        return (restaurant) => {
          return (restaurant.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
        };
      },  //获取数组数据
       loadIP() {
         axios.get(`http://127.0.0.1:5000/search`).then(res=>{console.log(res.data);this.IP_restaurants=res.data}).catch(err=>{console.log(err)})
      },
       IP_handleSelect(item) {
        this.ip_state=item.value;
        this.id_state=item.id;
//        console.log(item);
      },        //Ip遍历数组数据
       get_search_message(){
         axios.post(`http://127.0.0.1:5000/search`,{"id":this.id_state}).then(res=>{this.messages=res.data;this.$emit("Search_Button",this.messages)}).catch(err => {});
       },
       Select_Password(){
           if(this.select_password==true){
               this.select_password==false
             this.$emit("Select_Password_Button",this.select_password)
           }else {
               this.select_password==true
             this.$emit("Select_Password_Button",this.select_password)
           }
       }
     },
     created:function(){
         this.loadIP();      //Ip遍历数组数据
     }
   }

</script>

<style>
  .id{  text-overflow: ellipsis;  overflow: hidden;  font-size: 12px;  color: #b4b4b4}
  .username{font-size: 12px;  color: #b4b4b4;}
</style>
