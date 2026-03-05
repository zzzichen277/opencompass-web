<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue';
import * as echarts from 'echarts';
import type { EChartsOption } from 'echarts';

interface SeriesData {
  name: string;
  data: number[];
}

interface Props {
  categories: string[];
  series: SeriesData[];
  title?: string;
  height?: string | number;
}

const props = withDefaults(defineProps<Props>(), {
  title: '多模型对比',
  height: 400,
});

const chartRef = ref<HTMLElement | null>(null);
let chartInstance: echarts.ECharts | null = null;

const colors = ['#409EFF', '#67C23A', '#E6A23C', '#F56C6C', '#909399'];

const chartOption = computed<EChartsOption>(() => ({
  title: {
    text: props.title,
    left: 'center',
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'shadow',
    },
  },
  legend: {
    top: 'bottom',
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '15%',
    containLabel: true,
  },
  xAxis: {
    type: 'category',
    data: props.categories,
    axisLabel: {
      rotate: 30,
    },
  },
  yAxis: {
    type: 'value',
    max: 100,
  },
  series: props.series.map((s, index) => ({
    name: s.name,
    type: 'bar',
    data: s.data,
    itemStyle: {
      color: colors[index % colors.length],
    },
  })),
}));

function initChart() {
  if (chartRef.value) {
    chartInstance = echarts.init(chartRef.value);
    chartInstance.setOption(chartOption.value);
  }
}

function updateChart() {
  if (chartInstance) {
    chartInstance.setOption(chartOption.value);
  }
}

watch(() => [props.categories, props.series], updateChart, { deep: true });

onMounted(() => {
  initChart();
  window.addEventListener('resize', () => {
    chartInstance?.resize();
  });
});
</script>

<template>
  <div ref="chartRef" :style="{ height: typeof height === 'number' ? `${height}px` : height }" />
</template>