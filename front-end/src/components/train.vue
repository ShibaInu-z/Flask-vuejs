<template>
  <div>
   <div slot="header" class="clearfix">
     <button type="primary" @click="start_train" v-text="btn_train_text"> </button>
   </div>
   <div slot="header" class="clearfix">
     <h2 style="margin-left:10px;">训练过程记录</h2>
   </div>
   <div v-show="istrainging" slot="header" class="clearfix">
     <button type="primary" @click="start_tracing" v-text="btn_start_trace" > </button>
   </div>
   <div>
        <input v-model="train_log" rows="10" :readonly="true" :autosize="{ minRows: 15, maxRows: 30}" type="textarea" >
        <p>{{train_log}}</p>
   </div> 
  </div>
</template>

<script>
import axios from 'axios'
import moment from 'moment'

export default {
  name: 'train',
  data() {
    return {
      train_log: '',
      btn_train_text: '开始训练',
      btn_start_trace: '停止跟踪',
      istrainging: false,
      istracing: false,

      VGG_paras: {
        model_type: 'dl',
        name: 'VGG',
      },
      logs_paras: {
        app_name: 'flask_spark_dl',
        utc_str: '',
        VGG_paras: ''
      },
      timer: ''
    }
  },
  mounted() {
    const nowstr = moment().utc().format('YYYY-MM-DDTHH:mm:ss') + '.000GMT'
    console.log(nowstr)
  },
  methods: {
    onSubmit() {
      this.$message('submit!')
    },
    start_tracing() {
      this.istracing = !this.istracing
      if (this.istracing) { // 如果正在训练
        this.btn_start_trace = '停止跟踪'
        this.timer = setInterval(this.getTracingLogs, 7000) // 开启定时获取log
        this.$once('hook:beforeDestroy', () => {
          clearInterval(this.timer)
        })
      } else {
        this.btn_start_trace = '继续跟踪'
        clearInterval(this.timer)
      }
    },
    getTracingLogs() {
      console.log(this.VGG_paras)
      this.logs_paras.VGG_paras = this.VGG_paras
      get_logs(this.logs_paras).then(res => {
        if (res.data !== '') {
          this.train_log = res.data
        }
      })
    },
    start_train() {
      console.log(this.VGG_paras)
      const path = 'http://192.168.3.31:5000/api/train'
      const payload = {
        model_type: this.VGG_paras.model_type,
        name: this.VGG_paras.name
      }
       axios.post(path, payload)
         .then(res => {
            // content = res.data
            this.istrainging = true // 提交成功开始训练
            this.istracing = true
            this.logs_paras.utc_str = moment().utc().format('YYYY-MM-DDTHH:mm:ss') + '.000GMT'
            this.train_log = '正在启动集群，请稍后！'
            this.timer = setInterval(this.getTracingLogs, 6000) // 开启定时获取log
            console.log('start traning successfully!')
          })
    }
  }
}
</script>
