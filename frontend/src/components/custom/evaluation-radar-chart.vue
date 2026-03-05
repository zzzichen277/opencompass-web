<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue';
import * as echarts from 'echarts';
import type { EChartsOption } from 'echarts';

interface Props {
  data: Record<string, number>;
  title?: string;
  height?: string | number;
}

const props = withDefaults(defineProps<Props>(), {
  title: '模型能力雷达图',
  height: 400,
});

const chartRef = ref<HTMLElement | null>(null);
let chartInstance: echarts.ECharts | null = null;

const chartOption = computed<EChartsOption>(() => {
  const indicators = Object.keys(props.data).map(key => ({
    name: key,
    max: 100,
  }));

  return {
    title: {
      text: props.title,
      left: 'center',
    },
    tooltip: {
      trigger: 'item',
    },
    radar: {
      indicator: indicators,
      radius: '65%',
      axisName: {
        color: '#666',
      },
    },
    series: [
      {
        type: 'radar',
        data: [
          {
            value: Object.values(props.data),
            name: '得分',
            areaStyle: {
              color: 'rgba(64, 158, 255, 0.3)',
            },
            lineStyle: {
              color: '#409EFF',
              width: 2,
            },
            itemStyle: {
              color: '#409EFF',
            },
          },
        ],
      },
    ],
  };
});

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

watch(() => props.data, updateChart, { deep: true });

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