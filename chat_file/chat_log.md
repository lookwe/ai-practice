
---
**User**: vue3 性能优化有那些，分不用维度总结

**AI**:
# Vue3 性能优化策略

## 1. 编译时优化

### 1.1 静态提升 (Static Hoisting)
```javascript
// Vue 自动将静态节点提升到渲染函数外
const staticVNode = createVNode('div', { class: 'static' }, '静态内容')

export function render() {
  return staticVNode // 复用静态节点，避免重复创建
}
```

### 1.2 预字符串化 (Pre-stringification)
```javascript
// 连续的静态节点会被预编译为字符串
// 减少虚拟 DOM 的创建开销
```

## 2. 响应式系统优化

### 2.1 合理使用 ref 和 reactive
```javascript
// ❌ 不必要的响应式包装
const state = reactive({
  items: Array(1000).fill(0).map((_, i) => ({ id: i, name: `Item ${i}` }))
})

// ✅ 局部响应式，只对需要的属性进行响应式处理
const state = {
  items: Array(1000).fill(0).map((_, i) => ({ 
    id: i, 
    name: `Item ${i}`,
    // 只有需要响应式的属性才用 ref
    selected: ref(false) 
  }))
}
```

### 2.2 使用 shallowRef 和 shallowReactive
```javascript
// 对于大型对象或数组，使用浅层响应式
import { shallowReactive } from 'vue'

const state = shallowReactive({
  // 大型数据结构不会被深度代理
  largeData: new Array(10000).fill(0),
  // 需要响应式的属性单独处理
  count: 0
})
```

## 3. 组件级别优化

### 3.1 使用 Suspense 处理异步组件
```vue
<template>
  <Suspense>
    <template #default>
      <AsyncComponent />
    </template>
    <template #fallback>
      <div>加载中...</div>
    </template>
  </Suspense>
</template>

<script setup>
const AsyncComponent = defineAsyncComponent(() => 
  import('./HeavyComponent.vue')
)
</script>
```

### 3.2 组件懒加载
```javascript
// 路由级别的懒加载
const routes = [
  {
    path: '/heavy',
    component: () => import('./HeavyComponent.vue') // 按需加载
  }
]

// 组件内部懒加载
const HeavyComponent = defineAsyncComponent({
  loader: () => import('./HeavyComponent.vue'),
  loadingComponent: LoadingComponent,
  delay: 200
})
```

### 3.3 使用 keep-alive 缓存组件
```vue
<template>
  <!-- 缓存动态组件 -->
  <keep-alive :include="['ComponentA', 'ComponentB']">
    <component :is="currentComponent"></component>
  </keep-alive>
  
  <!-- 条件性缓存 -->
  <keep-alive :max="10"> <!-- 最多缓存10个组件 -->
    <component :is="currentComponent"></component>
  </keep-alive>
</template>
```

## 4. 渲染优化

### 4.1 使用 v-memo 优化列表渲染
```vue
<template>
  <!-- 只有当 item.id 或 item.name 改变时才重新渲染 -->
  <div v-for="item in list" :key="item.id" 
       v-memo="[item.id, item.name]">
    {{ item.name }}
  </div>
</template>
```

### 4.2 虚拟滚动优化长列表
```vue
<template>
  <VirtualList
    :items="largeList"
    :item-height="50"
    :visible-count="10"
    @scroll="handleScroll"
  >
    <template #item="{ item }">
      <ListItem :data="item" />
    </template>
  </VirtualList>
</template>

<script setup>
import VirtualList from './VirtualList.vue'
import { ref } from 'vue'

const largeList = ref(Array.from({ length: 10000 }, (_, i) => ({
  id: i,
  name: `Item ${i}`
})))
</script>
```

### 4.3 使用 Fragment 减少 DOM 层级
```vue
<template>
  <!-- Vue3 支持多个根节点，减少不必要的包装元素 -->
  <header>头部</header>
  <main>主要内容</main>
  <footer>底部</footer>
</template>
```

## 5. 网络请求优化

### 5.1 请求防抖和节流
```javascript
import { debounce } from 'lodash-es'
import { ref } from 'vue'

const searchQuery = ref('')
const searchResults = ref([])

// 防抖搜索
const debouncedSearch = debounce(async (query) => {
  if (query) {
    const results = await searchAPI(query)
    searchResults.value = results
  }
}, 300)

watch(searchQuery, debouncedSearch)
```

### 5.2 数据缓存策略
```javascript
// 使用 WeakMap 缓存计算结果
const cache = new WeakMap()

function expensiveCalculation(data) {
  if (cache.has(data)) {
    return cache.get(data)
  }
  
  const result = performExpensiveOperation(data)
  cache.set(data, result)
  return result
}
```

## 6. 打包构建优化

### 6.1 Tree Shaking 配置
```javascript
// vite.config.js
export default {
  build: {
    rollupOptions: {
      external: ['lodash'], // 外部化大型库
      output: {
        manualChunks: {
          vendor: ['vue', 'vue-router'],
          utils: ['lodash', 'axios']
        }
      }
    }
  }
}
```

### 6.2 代码分割
```javascript
// 动态导入实现代码分割
const loadModule = async (moduleName) => {
  const module = await import(`./modules/${moduleName}.js`)
  return module
}

// 路由级别的代码分割
{
  path: '/dashboard',
  component: () => import('./views/Dashboard.vue')
}
```

## 7. 监控和分析工具

### 7.1 性能监控
```javascript
// 使用 Performance API 监控组件渲染性能
import { onMounted } from 'vue'

export default {
  setup() {
    const startTime = performance.now()
    
    onMounted(() => {
      const endTime = performance.now()
      console.log(`组件渲染耗时: ${endTime - startTime}ms`)
    })
  }
}
```

### 7.2 使用 Vue DevTools 分析
```javascript
// 开发环境下启用性能标记
if (process.env.NODE_ENV === 'development') {
  performance.mark('component-setup-start')
  // 组件逻辑
  performance.mark('component-setup-end')
  performance.measure('setup-duration', 'component-setup-start', 'component-setup-end')
}
```

这些优化策略可以根据具体项目需求选择性应用，建议先通过性能分析工具定位瓶颈，再针对性地实施相应的优化措施。
