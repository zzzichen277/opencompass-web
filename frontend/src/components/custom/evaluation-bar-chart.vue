<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue';
import * as echarts from 'echarts';
import type { EChartsOption } from 'echarts';

interface DataItem {
  name: string;
  value: number;
  color?: string;
}

interface Props {
  data: DataItem[];
  title?: string;
  height?: string | number;
  horizontal?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  title: '模型得分对比',
  height: 400,
  horizontal: false,
});

const chartRef = ref<HTMLElement | null>(null);
let chartInstance: echarts.ECharts | null = null;

const chartOption = computed<EChartsOption>(() => {
  const names = props.data.map(d => d.name);
  const values = props.data.map(d => d.value);

  if (props.horizontal) {
    return {
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
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true,
      },
      xAxis: {
        type: 'value',
        max: 100,
      },
      yAxis: {
        type: 'category',
        data: names,
      },
      series: [
        {
          type: 'bar',
          data: values,
          itemStyle: {
            color: '#409EFF',
          },
          label: {
            show: true,
            position: 'right',
            formatter: '{c}%',
          },
        },
      ],
    };
  }

  return {
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
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      data: names,
      axisLabel: {
        rotate: 30,
      },
    },
    yAxis: {
      type: 'value',
      max: 100,
    },
    series: [
      {
        type: 'bar',
        data: values,
        itemStyle: {
          color: '#409EFF',
        },
        label: {
          show: true,
          position: 'top',
          formatter: '{c}%',
        },
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