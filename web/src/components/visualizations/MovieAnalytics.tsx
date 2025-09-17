import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import { motion } from 'framer-motion';

interface Movie {
  title: string;
  release_date: string;
  revenue_millions: number;
  vote_average: number;
  popularity: number;
  genres: string[];
}

interface MovieAnalyticsProps {
  data: Movie[];
}

interface GenreCount {
  genre: string;
  count: number;
}

export const MovieAnalytics = ({ data }: MovieAnalyticsProps): React.ReactElement => {
  const revenueChartRef = useRef<SVGSVGElement>(null);
  const genreChartRef = useRef<SVGSVGElement>(null);
  const ratingChartRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!data || !revenueChartRef.current) return;

    // Revenue Chart
    const margin = { top: 20, right: 30, bottom: 40, left: 90 };
    const width = 600 - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;

    const svg = d3.select(revenueChartRef.current);
    svg.selectAll("*").remove();

    const g = svg
      .append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    // Sort by revenue and get top 10
    const topMovies = [...data]
      .sort((a, b) => b.revenue_millions - a.revenue_millions)
      .slice(0, 10);

    const x = d3.scaleLinear()
      .domain([0, d3.max(topMovies, (d: Movie) => d.revenue_millions) || 0])
      .range([0, width]);

    const y = d3.scaleBand()
      .domain(topMovies.map((d: Movie) => d.title))
      .range([0, height])
      .padding(0.1);

    g.append("g")
      .attr("transform", `translate(0,${height})`)
      .call(d3.axisBottom(x))
      .selectAll("text")
      .style("text-anchor", "end")
      .attr("dx", "-.8em")
      .attr("dy", ".15em")
      .attr("transform", "rotate(-45)");

    g.append("g")
      .call(d3.axisLeft(y));

    g.selectAll("rect")
      .data(topMovies)
      .enter()
      .append("rect")
      .attr("y", (d: Movie) => y(d.title) || 0)
      .attr("height", y.bandwidth())
      .attr("fill", "#4C9AFF")
      .attr("x", 0)
      .attr("width", (d: Movie) => x(d.revenue_millions));
  }, [data]);

  useEffect(() => {
    if (!data || !genreChartRef.current) return;

    // Genre Chart
    const margin = { top: 20, right: 30, bottom: 40, left: 90 };
    const width = 400 - margin.left - margin.right;
    const height = 300 - margin.top - margin.bottom;

    const svg = d3.select(genreChartRef.current);
    svg.selectAll("*").remove();

    const g = svg
      .append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    // Count genres
    const genreCounts: { [key: string]: number } = {};
    data.forEach((movie: Movie) => {
      movie.genres.forEach((genre: string) => {
        genreCounts[genre] = (genreCounts[genre] || 0) + 1;
      });
    });

    const genreData = Object.entries(genreCounts)
      .map(([genre, count]): GenreCount => ({ genre, count }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 8);

    const x = d3.scaleLinear()
      .domain([0, d3.max(genreData, (d: GenreCount) => d.count) || 0])
      .range([0, width]);

    const y = d3.scaleBand()
      .domain(genreData.map((d: GenreCount) => d.genre))
      .range([0, height])
      .padding(0.1);

    g.append("g")
      .attr("transform", `translate(0,${height})`)
      .call(d3.axisBottom(x));

    g.append("g")
      .call(d3.axisLeft(y));

    g.selectAll("rect")
      .data(genreData)
      .enter()
      .append("rect")
      .attr("y", (d: GenreCount) => y(d.genre) || 0)
      .attr("height", y.bandwidth())
      .attr("fill", "#50C878")
      .attr("x", 0)
      .attr("width", (d: GenreCount) => x(d.count));
  }, [data]);

  useEffect(() => {
    if (!data || !ratingChartRef.current) return;

    // Rating vs Popularity Chart
    const margin = { top: 20, right: 30, bottom: 40, left: 50 };
    const width = 400 - margin.left - margin.right;
    const height = 300 - margin.top - margin.bottom;

    const svg = d3.select(ratingChartRef.current);
    svg.selectAll("*").remove();

    const g = svg
      .append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    const x = d3.scaleLinear()
      .domain([0, 10])
      .range([0, width]);

    const y = d3.scaleLinear()
      .domain([0, d3.max(data, (d: Movie) => d.popularity) || 0])
      .range([height, 0]);

    g.append("g")
      .attr("transform", `translate(0,${height})`)
      .call(d3.axisBottom(x));

    g.append("g")
      .call(d3.axisLeft(y));

    g.selectAll("circle")
      .data(data)
      .enter()
      .append("circle")
      .attr("cx", (d: Movie) => x(d.vote_average))
      .attr("cy", (d: Movie) => y(d.popularity))
      .attr("r", 5)
      .attr("fill", "#FF6B6B")
      .attr("opacity", 0.6);
  }, [data]);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="space-y-8 p-4"
    >
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-xl font-bold mb-4">Top 10 Highest Grossing Disney Movies</h3>
        <svg
          ref={revenueChartRef}
          width="600"
          height="400"
          className="w-full"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold mb-4">Genre Distribution</h3>
          <svg
            ref={genreChartRef}
            width="400"
            height="300"
            className="w-full"
          />
        </div>

        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold mb-4">Rating vs Popularity</h3>
          <svg
            ref={ratingChartRef}
            width="400"
            height="300"
            className="w-full"
          />
        </div>
      </div>
    </motion.div>
  );
}; 