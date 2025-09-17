'use client';

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ChartOptions
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

interface BoxOfficeData {
  title: string;
  budget: number;
  revenue: number;
  profit: number;
}

interface BoxOfficeChartProps {
  data: BoxOfficeData[];
}

export default function BoxOfficeChart({ data }: BoxOfficeChartProps) {
  const chartData = {
    labels: data.map(movie => movie.title),
    datasets: [
      {
        label: 'Budget',
        data: data.map(movie => movie.budget),
        backgroundColor: 'rgba(0, 119, 200, 0.6)', // Disney blue
      },
      {
        label: 'Revenue',
        data: data.map(movie => movie.revenue),
        backgroundColor: 'rgba(255, 184, 28, 0.6)', // Disney yellow
      },
      {
        label: 'Profit',
        data: data.map(movie => movie.profit),
        backgroundColor: 'rgba(123, 67, 151, 0.6)', // Disney purple
      },
    ],
  };

  const options: ChartOptions<'bar'> = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Box Office Performance',
        font: {
          size: 16,
          family: 'var(--font-playfair-display)',
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Amount (USD)',
        },
        ticks: {
          callback: (value) => {
            return `$${(Number(value) / 1000000).toFixed(0)}M`;
          },
        },
      },
    },
  };

  return (
    <div className="w-full rounded-lg bg-white p-4 shadow-lg">
      <Bar options={options} data={chartData} />
    </div>
  );
} 