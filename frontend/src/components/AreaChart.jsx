import { Line } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

const AreaChart = ({ data, title }) => {
  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: 'top',
        labels: {
          color: '#9ba1b4',
          font: {
            size: 12
          }
        }
      },
      title: {
        display: true,
        text: title,
        color: '#e1e4ed',
        font: {
          size: 16,
          weight: 'bold'
        }
      },
      tooltip: {
        backgroundColor: '#141824',
        borderColor: '#2a3142',
        borderWidth: 1,
        titleColor: '#e1e4ed',
        bodyColor: '#9ba1b4',
        padding: 12,
        displayColors: true,
      }
    },
    scales: {
      x: {
        grid: {
          color: '#2a3142',
          borderColor: '#2a3142',
        },
        ticks: {
          color: '#9ba1b4',
        }
      },
      y: {
        grid: {
          color: '#2a3142',
          borderColor: '#2a3142',
        },
        ticks: {
          color: '#9ba1b4',
        }
      }
    },
    interaction: {
      intersect: false,
      mode: 'index',
    }
  }

  return (
    <div className="h-full w-full">
      <Line data={data} options={options} />
    </div>
  )
}

export default AreaChart
