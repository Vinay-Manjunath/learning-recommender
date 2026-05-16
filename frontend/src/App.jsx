import { useState } from "react";
import axios from "axios";

function App() {

  const [query, setQuery] = useState("");
  const [difficulty, setDifficulty] = useState("Beginner");

  const [courses, setCourses] = useState([]);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  // -----------------------------------------
  // Fetch recommendations from backend
  // -----------------------------------------

  const getRecommendations = async () => {

    if (!query.trim()) {
      setError("Please enter a search query");
      return;
    }

    setLoading(true);

    setError("");

    try {

      const response = await axios.post(
        "http://localhost:8001/recommend",
        {
          query,
          difficulty,
          top_n: 5
        }
      );

      setCourses(response.data);

    } catch (err) {

      console.error(err);

      setError("Failed to fetch recommendations");

    } finally {

      setLoading(false);
    }
  };

  return (

    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-gray-100 to-purple-100 p-10">

      <div className="max-w-5xl mx-auto">

        {/* Header */}

        <div className="text-center mb-10">

          <h1 className="text-6xl font-extrabold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-4">
            Personalized Learning Recommender
          </h1>

          <p className="text-gray-600 text-lg">
            Discover the best learning paths using AI-powered recommendations
          </p>

        </div>

        {/* Search Section */}

        <div className="bg-white/70 backdrop-blur-md rounded-3xl shadow-2xl p-6 mb-10 border border-white/30">

          <div className="flex flex-col md:flex-row gap-4">

            {/* Search Input */}

            <input
              type="text"
              placeholder="Search courses like machine learning, python, AI..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  getRecommendations();
                }
              }}
              className="flex-1 border border-gray-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />

            {/* Difficulty Dropdown */}

            <select
              value={difficulty}
              onChange={(e) => setDifficulty(e.target.value)}
              className="border border-gray-300 rounded-xl px-4 py-3"
            >

              <option>Beginner</option>
              <option>Intermediate</option>
              <option>Advanced</option>
              <option>Mixed</option>

            </select>

            {/* Button */}

            <button
              onClick={getRecommendations}
              className="bg-gradient-to-r from-blue-600 to-purple-600 hover:scale-105 hover:shadow-xl text-white px-6 py-3 rounded-xl font-semibold transition duration-300"
            >
              Recommend
            </button>

          </div>

          {/* Error */}

          {error && (
            <p className="text-red-500 mt-4">
              {error}
            </p>
          )}

        </div>

        {/* Loading */}

        {loading && (

          <div className="flex justify-center items-center py-10">

            <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600"></div>

          </div>

        )}

        {/* Empty State */}

        {!loading && courses.length === 0 && (

          <div className="text-center py-20 text-gray-500">

            <h2 className="text-3xl font-bold mb-4">
              Start Exploring Courses 🚀
            </h2>

            <p className="text-lg">
              Search for topics like AI, Python, Machine Learning, Data Science...
            </p>
          </div>
        )}

        {/* Recommendation Cards */}

        <div className="grid md:grid-cols-2 gap-6">

          {courses.map((course, index) => (

            <div
              key={index}
              className="bg-white/80 backdrop-blur-md rounded-3xl shadow-xl p-6 hover:shadow-2xl hover:-translate-y-3 hover:scale-[1.02] transition duration-300 border border-white/30"
            >

              <h2 className="text-2xl font-bold text-gray-800 mb-3">
                {course.course_title}
              </h2>

              <p className="text-gray-600 mb-4">
                {course.course_organization}
              </p>

              <div className="flex flex-wrap gap-3 text-sm">

                <span className="bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full">
                  ⭐ {course.rating}
                </span>

                <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full">
                  👥 {Math.round(course.enrollment).toLocaleString()}
                </span>

                <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full">
                  {course.course_difficulty}
                </span>

                <span className="bg-purple-100 text-purple-800 px-3 py-1 rounded-full">
                  {Math.round(course.similarity * 100)}% Match
                </span>

              </div>

            </div>

          ))}

        </div>

      </div>

    </div>
  );
}

export default App;
