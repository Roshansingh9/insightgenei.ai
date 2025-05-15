import Header from "./components/Header";
import CustomFooter from "./components/Footer";

function App() {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Fixed Header sits on top */}
      <Header />

      {/* Main content area */}
      <main className="flex-1 pt-24 px-4 sm:px-6 lg:px-8 max-w-screen-xl mx-auto w-full bg-black text-white">
        {/* Replace bg-0a0a0a with inline style or custom class */}
        <div style={{ backgroundColor: "#0a0a0a" }} className="p-4 rounded">
          <h1 className="text-3xl font-bold">Hello</h1>
        </div>
      </main>

      <CustomFooter />
    </div>
  );
}

export default App;
