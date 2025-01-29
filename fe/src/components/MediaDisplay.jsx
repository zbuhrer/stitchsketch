function MediaDisplay({ item }) {
  const renderMedia = () => {
    switch (item.type) {
      case "image":
        return <img src={item.url} alt={item.description} />;
      case "video":
        return (
          <video controls>
            <source src={item.url} type={item.mimeType} />
            Your browser does not support video playback.
          </video>
        );
      default:
        return <div>Unsupported media type</div>;
    }
  };

  return (
    <div className="media-item">
      {renderMedia()}
      <p>{item.description}</p>
    </div>
  );
}

export default MediaDisplay;
