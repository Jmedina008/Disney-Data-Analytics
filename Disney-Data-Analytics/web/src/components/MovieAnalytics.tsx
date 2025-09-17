import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';

interface Movie {
  title: string;
  budget: number;
  revenue: number;
  studio: string;
  release_year: number;
}

interface MovieAnalyticsProps {
  width?: number;
  height?: number;
}

export const MovieAnalytics: React.FC<MovieAnalyticsProps> = ({ 
  width = 800, 
  height = 600 
}) => {
  const svgRef = useRef<SVGSVGElement>(null);
  const [data, setData] = useState<Movie[]>([]);
  const [selectedStudio, setSelectedStudio] = useState<string>('All');
  const [loading, setLoading] = useState(true);
  const [view, setView] = useState<'revenue' | 'roi' | 'scatter'>('revenue');

  // Load data on component mount
  useEffect(() => {
    const loadData = async () => {
      try {
        // Simulate loading from CSV (in real app, this would fetch from API)
        const sampleData: Movie[] = [
          { title: "Marvel: Adventure 1", budget: 150000000, revenue: 850000000, studio: "Marvel", release_year: 2023 },
          { title: "Pixar: Quest 2", budget: 200000000, revenue: 600000000, studio: "Pixar", release_year: 2022 },
          { title: "Disney's Magic 3", budget: 120000000, revenue: 400000000, studio: "Disney", release_year: 2023 },
          { title: "Marvel: Hero 4", budget: 180000000, revenue: 950000000, studio: "Marvel", release_year: 2024 },
          { title: "Pixar: Journey 5", budget: 160000000, revenue: 550000000, studio: "Pixar", release_year: 2021 },
          { title: "Disney's Princess 6", budget: 90000000, revenue: 320000000, studio: "Disney", release_year: 2022 },
          { title: "Marvel: Quest 7", budget: 200000000, revenue: 1200000000, studio: "Marvel", release_year: 2023 },
          { title: "Pixar: Dream 8", budget: 140000000, revenue: 480000000, studio: "Pixar", release_year: 2024 },
          { title: "Disney's Kingdom 9", budget: 110000000, revenue: 380000000, studio: "Disney", release_year: 2021 },
          { title: "Marvel: Adventure 10", budget: 170000000, revenue: 750000000, studio: "Marvel", release_year: 2022 }
        ];
        
        setData(sampleData);
        setLoading(false);
      } catch (error) {
        console.error('Error loading data:', error);
        setLoading(false);
      }
    };

    loadData();
  }, []);

  // Filter data based on selected studio
  const filteredData = selectedStudio === 'All' 
    ? data 
    : data.filter(d => d.studio === selectedStudio);

  // Create visualizations
  useEffect(() => {
    if (!data.length || !svgRef.current) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove();

    const margin = { top: 50, right: 100, bottom: 80, left: 80 };
    const chartWidth = width - margin.left - margin.right;
    const chartHeight = height - margin.top - margin.bottom;

    const g = svg.append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    // Color scale for studios
    const colorScale = d3.scaleOrdinal<string>()
      .domain(['Marvel', 'Pixar', 'Disney'])
      .range(['#FF6B6B', '#4ECDC4', '#45B7D1']);

    if (view === 'revenue') {
      // Revenue Bar Chart
      const sortedData = [...filteredData]
        .sort((a, b) => b.revenue - a.revenue)
        .slice(0, 8); // Top 8 movies

      const x = d3.scaleBand()
        .domain(sortedData.map(d => d.title))
        .range([0, chartWidth])
        .padding(0.1);

      const y = d3.scaleLinear()
        .domain([0, d3.max(sortedData, d => d.revenue) || 0])
        .range([chartHeight, 0]);

      // Add axes
      g.append("g")
        .attr("transform", `translate(0,${chartHeight})`)
        .call(d3.axisBottom(x))
        .selectAll("text")
        .attr("transform", "rotate(-45)")
        .style("text-anchor", "end")
        .style("font-size", "10px");

      g.append("g")
        .call(d3.axisLeft(y)
          .tickFormat(d => `$${(d as number / 1000000).toFixed(0)}M`));

      // Add bars with animation
      const bars = g.selectAll(".bar")
        .data(sortedData)
        .enter().append("rect")
        .attr("class", "bar")
        .attr("x", d => x(d.title) || 0)
        .attr("width", x.bandwidth())
        .attr("y", chartHeight)
        .attr("height", 0)
        .attr("fill", d => colorScale(d.studio))
        .attr("opacity", 0.8);

      // Animate bars
      bars.transition()
        .duration(1000)
        .attr("y", d => y(d.revenue))
        .attr("height", d => chartHeight - y(d.revenue));

      // Add hover effects
      bars
        .on("mouseover", function(event, d) {
          d3.select(this).attr("opacity", 1);
          
          // Tooltip
          const tooltip = g.append("g")
            .attr("class", "tooltip")
            .attr("transform", `translate(${(x(d.title) || 0) + x.bandwidth()/2}, ${y(d.revenue) - 10})`);
          
          tooltip.append("rect")
            .attr("x", -50)
            .attr("y", -30)
            .attr("width", 100)
            .attr("height", 25)
            .attr("fill", "black")
            .attr("opacity", 0.8)
            .attr("rx", 5);
          
          tooltip.append("text")
            .attr("text-anchor", "middle")
            .attr("y", -10)
            .attr("fill", "white")
            .style("font-size", "12px")
            .text(`$${(d.revenue / 1000000).toFixed(0)}M`);
        })
        .on("mouseout", function() {
          d3.select(this).attr("opacity", 0.8);
          g.select(".tooltip").remove();
        });

      // Add title
      g.append("text")
        .attr("x", chartWidth / 2)
        .attr("y", -20)
        .attr("text-anchor", "middle")
        .style("font-size", "16px")
        .style("font-weight", "bold")
        .text(`Disney Movie Revenue Performance${selectedStudio !== 'All' ? ` - ${selectedStudio}` : ''}`);

      // Add axis labels
      g.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left)
        .attr("x", 0 - (chartHeight / 2))
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .text("Revenue (Millions $)");

    } else if (view === 'scatter') {
      // Budget vs Revenue Scatter Plot
      const x = d3.scaleLinear()
        .domain([0, d3.max(filteredData, d => d.budget) || 0])
        .range([0, chartWidth]);

      const y = d3.scaleLinear()
        .domain([0, d3.max(filteredData, d => d.revenue) || 0])
        .range([chartHeight, 0]);

      // Add axes
      g.append("g")
        .attr("transform", `translate(0,${chartHeight})`)
        .call(d3.axisBottom(x)
          .tickFormat(d => `$${(d as number / 1000000).toFixed(0)}M`));

      g.append("g")
        .call(d3.axisLeft(y)
          .tickFormat(d => `$${(d as number / 1000000).toFixed(0)}M`));

      // Add break-even line
      const maxValue = Math.max(
        d3.max(filteredData, d => d.budget) || 0,
        d3.max(filteredData, d => d.revenue) || 0
      );
      
      g.append("line")
        .attr("x1", 0)
        .attr("y1", chartHeight)
        .attr("x2", x(maxValue))
        .attr("y2", y(maxValue))
        .attr("stroke", "#999")
        .attr("stroke-dasharray", "5,5")
        .attr("opacity", 0.6);

      // Add scatter points
      const circles = g.selectAll(".circle")
        .data(filteredData)
        .enter().append("circle")
        .attr("class", "circle")
        .attr("cx", d => x(d.budget))
        .attr("cy", d => y(d.revenue))
        .attr("r", 0)
        .attr("fill", d => colorScale(d.studio))
        .attr("opacity", 0.7)
        .attr("stroke", "white")
        .attr("stroke-width", 2);

      // Animate circles
      circles.transition()
        .duration(1000)
        .attr("r", 8);

      // Add hover effects
      circles
        .on("mouseover", function(event, d) {
          d3.select(this).attr("r", 12).attr("opacity", 1);
          
          const tooltip = g.append("g")
            .attr("class", "tooltip")
            .attr("transform", `translate(${x(d.budget) + 15}, ${y(d.revenue) - 15})`);
          
          tooltip.append("rect")
            .attr("x", 0)
            .attr("y", -40)
            .attr("width", 120)
            .attr("height", 35)
            .attr("fill", "black")
            .attr("opacity", 0.9)
            .attr("rx", 5);
          
          tooltip.append("text")
            .attr("x", 5)
            .attr("y", -25)
            .attr("fill", "white")
            .style("font-size", "11px")
            .text(d.title.length > 15 ? d.title.substring(0, 15) + "..." : d.title);
          
          tooltip.append("text")
            .attr("x", 5)
            .attr("y", -10)
            .attr("fill", "white")
            .style("font-size", "10px")
            .text(`ROI: ${(((d.revenue - d.budget) / d.budget) * 100).toFixed(0)}%`);
        })
        .on("mouseout", function() {
          d3.select(this).attr("r", 8).attr("opacity", 0.7);
          g.select(".tooltip").remove();
        });

      // Add title and labels
      g.append("text")
        .attr("x", chartWidth / 2)
        .attr("y", -20)
        .attr("text-anchor", "middle")
        .style("font-size", "16px")
        .style("font-weight", "bold")
        .text(`Budget vs Revenue Analysis${selectedStudio !== 'All' ? ` - ${selectedStudio}` : ''}`);

      g.append("text")
        .attr("x", chartWidth / 2)
        .attr("y", chartHeight + margin.bottom - 20)
        .attr("text-anchor", "middle")
        .text("Budget (Millions $)");

      g.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left)
        .attr("x", 0 - (chartHeight / 2))
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .text("Revenue (Millions $)");
    }

    // Add legend
    const legend = svg.append("g")
      .attr("class", "legend")
      .attr("transform", `translate(${width - 90}, 60)`);

    const studios = ['Marvel', 'Pixar', 'Disney'];
    const legendItems = legend.selectAll(".legend-item")
      .data(studios)
      .enter().append("g")
      .attr("class", "legend-item")
      .attr("transform", (d, i) => `translate(0, ${i * 20})`);

    legendItems.append("circle")
      .attr("cx", 0)
      .attr("cy", 0)
      .attr("r", 6)
      .attr("fill", d => colorScale(d));

    legendItems.append("text")
      .attr("x", 12)
      .attr("y", 0)
      .attr("dy", "0.35em")
      .style("font-size", "12px")
      .text(d => d);

  }, [data, selectedStudio, view, width, height]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-lg">Loading Disney movie data...</div>
      </div>
    );
  }

  const studios = ['All', ...Array.from(new Set(data.map(d => d.studio)))];

  return (
    <div className="w-full bg-white rounded-lg shadow-lg p-6">
      <div className="mb-4 flex flex-wrap gap-4 justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-gray-800">Disney Movie Analytics</h2>
          <p className="text-gray-600">Interactive analysis of Disney studio performance</p>
        </div>
        
        <div className="flex gap-4">
          <select
            value={selectedStudio}
            onChange={(e) => setSelectedStudio(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {studios.map(studio => (
              <option key={studio} value={studio}>{studio}</option>
            ))}
          </select>
          
          <div className="flex rounded-lg border border-gray-300 overflow-hidden">
            <button
              onClick={() => setView('revenue')}
              className={`px-4 py-2 text-sm ${view === 'revenue' ? 'bg-blue-500 text-white' : 'bg-white text-gray-700 hover:bg-gray-50'}`}
            >
              Revenue
            </button>
            <button
              onClick={() => setView('scatter')}
              className={`px-4 py-2 text-sm ${view === 'scatter' ? 'bg-blue-500 text-white' : 'bg-white text-gray-700 hover:bg-gray-50'}`}
            >
              Budget vs Revenue
            </button>
          </div>
        </div>
      </div>
      
      <div className="w-full overflow-x-auto">
        <svg
          ref={svgRef}
          width={width}
          height={height}
          className="w-full h-auto"
          viewBox={`0 0 ${width} ${height}`}
        />
      </div>
      
      <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
        <div className="bg-gray-50 p-3 rounded">
          <div className="font-semibold text-gray-700">Total Movies</div>
          <div className="text-2xl font-bold text-blue-600">{filteredData.length}</div>
        </div>
        <div className="bg-gray-50 p-3 rounded">
          <div className="font-semibold text-gray-700">Avg Revenue</div>
          <div className="text-2xl font-bold text-green-600">
            ${(filteredData.reduce((sum, d) => sum + d.revenue, 0) / filteredData.length / 1000000).toFixed(0)}M
          </div>
        </div>
        <div className="bg-gray-50 p-3 rounded">
          <div className="font-semibold text-gray-700">Avg ROI</div>
          <div className="text-2xl font-bold text-purple-600">
            {(filteredData.reduce((sum, d) => sum + ((d.revenue - d.budget) / d.budget * 100), 0) / filteredData.length).toFixed(0)}%
          </div>
        </div>
      </div>
    </div>
  );
};