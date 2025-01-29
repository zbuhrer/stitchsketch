class ErrorBoundary extends React.Component {
  state = { hasError: false };

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-container">
          <h3>Something went wrong displaying this content.</h3>
          <button onClick={() => window.location.reload()}>Refresh Page</button>
        </div>
      );
    }

    return this.props.children;
  }
}
