/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{html,jsx}"],
  theme: {
    extend: {
      colors: {
        pink_title: "#DE55DE",
        input_bg: "#1C1F28",
        input_border: "#EC83BB",
        input_shadow: "#B664DB",
        bg_result: "#100c23",
        doc_title: "#FFB4FF",
        bg_select: "rgba(42, 24, 56, 0.7)",
      },
    },
  },
  plugins: [],
};
