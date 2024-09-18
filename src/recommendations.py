import pandas as pd
import chardet

def process_chunk(chunk):
    # Aquí puedes añadir la lógica para procesar cada chunk
    return chunk

def detect_encoding(file_path):
    try:
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())
        return result['encoding']
    except Exception as e:
        print(f"Error al detectar la codificación del archivo: {e}")
        return None

def get_data_from_csv(file_path, chunk_size=10000):
    try:
        encoding = detect_encoding(file_path)
        if encoding is None:
            raise ValueError("No se pudo detectar la codificación del archivo.")

        chunks = []
        for chunk in pd.read_csv(file_path, chunksize=chunk_size, encoding=encoding):
            processed_chunk = process_chunk(chunk)
            chunks.append(processed_chunk)

        # Combina todos los chunks procesados en un solo DataFrame
        data = pd.concat(chunks, ignore_index=True)
        return data
    except pd.errors.EmptyDataError:
        print("El archivo CSV está vacío.")
    except pd.errors.ParserError:
        print("Error al analizar el archivo CSV.")
    except FileNotFoundError:
        print(f"El archivo {file_path} no se encontró.")
    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(f"Se produjo un error inesperado: {e}")
    return None

def recommend_based_on_recent(recent_tracks, all_tracks, top_n=10):
    """
    Genera recomendaciones basadas en las últimas canciones escuchadas.
    """
    try:
        # Verifica que las columnas existan
        required_columns = ['energy', 'danceability', 'tempo']
        for col in required_columns:
            if col not in all_tracks.columns:
                raise KeyError(f"La columna '{col}' no se encuentra en el DataFrame.")

        recommendations = []
        for _, recent_track in recent_tracks.iterrows():
            similar_tracks = all_tracks[
                (all_tracks['energy'] >= recent_track['energy'] - 0.1) &
                (all_tracks['energy'] <= recent_track['energy'] + 0.1) &
                (all_tracks['danceability'] >= recent_track['danceability'] - 0.1) &
                (all_tracks['danceability'] <= recent_track['danceability'] + 0.1) &
                (all_tracks['tempo'] >= recent_track['tempo'] - 10) &
                (all_tracks['tempo'] <= recent_track['tempo'] + 10)
            ]
            recommendations.extend(similar_tracks.head(top_n).to_dict('records'))
        return recommendations
    except KeyError as ke:
        print(ke)
        return []
    except Exception as e:
        print(f"Se produjo un error inesperado: {e}")
        return []

def recommend_new_tracks(all_tracks, top_n=10):
    """
    Genera nuevas recomendaciones basadas en parámetros como "energy", "danceability" y "tempo".
    """
    try:
        new_recommendations = all_tracks.sample(n=top_n).to_dict('records')
        return new_recommendations
    except Exception as e:
        print(f"Se produjo un error inesperado: {e}")
        return []

def create_playlist(recommendations, playlist_name="New Playlist"):
    """
    Crea una nueva lista de reproducción con las recomendaciones.
    """
    playlist = pd.DataFrame(recommendations)
    print(f"\n{playlist_name}:")
    print(playlist[['track_name', 'track_artists', 'track_album_name', 'energy', 'danceability', 'tempo']])
    return playlist

# Ejemplo de uso
if __name__ == "__main__":
    from data_processing import get_data_from_csv

    recent_tracks_file_path = './data/User_A.csv'
    spotify_songs_file_path = './data/spotify_songs.csv'

    recent_tracks = get_data_from_csv(recent_tracks_file_path)
    all_tracks = get_data_from_csv(spotify_songs_file_path)

    if recent_tracks is not None and all_tracks is not None:
        print("Columnas en all_tracks:", all_tracks.columns)
        recent_recommendations = recommend_based_on_recent(recent_tracks, all_tracks)
        new_track_recommendations = recommend_new_tracks(all_tracks)

        print("Recomendaciones basadas en tus últimas canciones escuchadas:")
        for rec in recent_recommendations:
            print(rec)

        print("\nNuevas recomendaciones:")
        for rec in new_track_recommendations:
            print(rec)

        # Crear y mostrar la nueva lista de reproducción
        playlist = create_playlist(recent_recommendations, "Playlist Basada en Tus Últimas Canciones Escuchadas")
    else:
        print("No se pudo procesar uno o ambos archivos CSV.")
