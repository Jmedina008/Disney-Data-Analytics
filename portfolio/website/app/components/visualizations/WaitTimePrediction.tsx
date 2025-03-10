'use client';

import { useEffect, useRef } from 'react';
import * as d3 from 'd3';

interface WaitTimeData {
  hour: number;
  actual: number;
  predicted: number;
}

interface WaitTimePredictionProps {
  data: WaitTimeData[];
  attractionName: string;
}

export default function WaitTimePrediction({ data, attractionName }: WaitTimePredictionProps) {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!svgRef.current || !data) return;

    const margin = { top: 20, right: 30, bottom: 40, left: 40 };
    const width = 600 - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;

    // Clear existing SVG
    d3.select(svgRef.current).selectAll('*').remove();

    const svg = d3.select(svgRef.current)
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // Scales
    const x = d3.scaleLinear()
      .domain([0, 23])
      .range([0, width]);

    const y = d3.scaleLinear()
      .domain([0, d3.max(data, d => Math.max(d.actual, d.predicted)) || 0])
      .range([height, 0]);

    // Lines
    const actualLine = d3.line<WaitTimeData>()
      .x(d => x(d.hour))
      .y(d => y(d.actual));

    const predictedLine = d3.line<WaitTimeData>()
      .x(d => x(d.hour))
      .y(d => y(d.predicted));

    // Add lines
    svg.append('path')
      .datum(data)
      .attr('fill', 'none')
      .attr('stroke', '#0077C8')
      .attr('stroke-width', 2)
      .attr('d', actualLine);

    svg.append('path')
      .datum(data)
      .attr('fill', 'none')
      .attr('stroke', '#FFB81C')
      .attr('stroke-dasharray', '5,5')
      .attr('stroke-width', 2)
      .attr('d', predictedLine);

    // Add axes
    svg.append('g')
      .attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(x).ticks(24));

    svg.append('g')
      .call(d3.axisLeft(y));

    // Add labels
    svg.append('text')
      .attr('x', width / 2)
      .attr('y', height + margin.bottom - 5)
      .attr('text-anchor', 'middle')
      .text('Hour of Day');

    svg.append('text')
      .attr('transform', 'rotate(-90)')
      .attr('x', -height / 2)
      .attr('y', -margin.left + 10)
      .attr('text-anchor', 'middle')
      .text('Wait Time (minutes)');

    // Add legend
    const legend = svg.append('g')
      .attr('transform', `translate(${width - 100}, 0)`);

    legend.append('line')
      .attr('x1', 0)
      .attr('x2', 20)
      .attr('y1', 0)
      .attr('y2', 0)
      .attr('stroke', '#0077C8')
      .attr('stroke-width', 2);

    legend.append('line')
      .attr('x1', 0)
      .attr('x2', 20)
      .attr('y1', 20)
      .attr('y2', 20)
      .attr('stroke', '#FFB81C')
      .attr('stroke-width', 2)
      .attr('stroke-dasharray', '5,5');

    legend.append('text')
      .attr('x', 25)
      .attr('y', 4)
      .text('Actual');

    legend.append('text')
      .attr('x', 25)
      .attr('y', 24)
      .text('Predicted');

  }, [data]);

  return (
    <div className="w-full rounded-lg bg-white p-4 shadow-lg">
      <h3 className="mb-4 font-display text-xl font-bold text-disney-gray">
        {attractionName} - Wait Time Prediction
      </h3>
      <svg ref={svgRef} className="mx-auto"></svg>
    </div>
  );
} 