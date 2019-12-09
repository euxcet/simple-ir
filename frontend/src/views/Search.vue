<template>
  <div class="main">
    <h1>{{msg}}</h1>
    <div class="search-bar">
      <el-form :model="form">
        <el-input class="form-input" placeholder clearable v-model.trim="form.word"></el-input>
      </el-form>
      <el-button class="form-button" size="small" type="primary" @click="submit">Button</el-button>
      <el-checkbox class="form-checkbox" :indeterminate="isIndeterminate" v-model="checkAll" @change="handleCheckAllChange">全选</el-checkbox>
      <el-checkbox-group class="form-checkbox-group" v-model="checkedClass" @change="handleCheckedChange">
        <el-checkbox v-for="option in options" :label="option" :key="option"> {{option}} </el-checkbox>
      </el-checkbox-group>
      <div class="form-window">
        <label>检索词与关键词距离</label>
        <el-input-number v-model="window" :min=1 :max=4 label="距离"></el-input-number>
      </div>
    </div>
    <div class="result">
      <el-table :data="result">
        <el-table-column prop="phrase" label="词组" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="doc" label="文档" header-align="center" align="center">
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
const classOptions = ['名词', '人名', '地名', '机构名', '其它专名', '数词', '量词', '数量词', '时间词', '方位词', '处所词', '动词', '形容词', '副词', '前接成分', '后接成分', '习语', '简称', '代词', '连词', '介词', '助词', '语气助词', '叹词', '拟声词', '语素', '标点', '其它']
export default {
  name: 'Search',
  data () {
    return {
      msg: 'Information Retrieval System',
      url: 'http://127.0.0.1:5000/search',
      result: [],
      form: {
        word: ''
      },
      window: 1,
      checkAll: true,
      checkedClass: classOptions,
      options: classOptions,
      isIndeterminate: false
    }
  },
  methods: {
    handleCheckAllChange (val) {
      this.checkedClass = val ? this.options : []
      this.isIndeterminate = false
    },
    handleCheckedChange (val) {
      let count = val.length
      this.checkAll = count === this.options.length
      this.isIndeterminate = count > 0 && count < this.options.length
    },
    submit () {
      axios.post(this.url, { 'word': this.form.word, 'option': this.checkedClass, 'window': this.window }, {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      }).then(response => (this.result = response.data.pair))
    }
  }
}
</script>
