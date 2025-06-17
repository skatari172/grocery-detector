import React, { useState } from 'react';
import {
  SafeAreaView,
  ScrollView,
  View,
  Button,
  Image,
  Text,
  ActivityIndicator,
  StyleSheet,
} from 'react-native';
import { launchImageLibrary, Asset } from 'react-native-image-picker';
import axios from 'axios';

export default function App() {
  const [photo, setPhoto] = useState<Asset | null>(null);
  const [result, setResult] = useState<any>(null);
  const [uploading, setUploading] = useState(false);

  const pickImage = () => {
    launchImageLibrary(
      { mediaType: 'photo' },
      response => {
        if (response.didCancel) return;
        if (response.errorCode) {
          console.error('ImagePicker Error: ', response.errorMessage);
          return;
        }
        if (response.assets?.length) {
          setPhoto(response.assets[0]);
          setResult(null);
        }
      }
    );
  };

  const uploadImage = async () => {
    if (!photo?.uri) return;
    setUploading(true);

    const formData = new FormData();
    formData.append('file', {
      uri: photo.uri,
      name: photo.fileName || 'photo.jpg',
      type: photo.type || 'image/jpeg',
    } as any);

    try {
      const res = await axios.post(
        'http://YOUR_LOCAL_IP:4000/predict',
        formData,
        { headers: { 'Content-Type': 'multipart/form-data' } }
      );
      setResult(res.data);
    } catch {
      setResult({ error: 'Upload failed' });
    } finally {
      setUploading(false);
    }
  };

  return (
    <SafeAreaView style={styles.safe}>
      <ScrollView contentContainerStyle={styles.container}>
        <Text style={styles.title}>Grocery Shelf Classifier</Text>
        <Text style={styles.subtitle}>
          Take a photo of your grocery shelf and see what products are detected.
        </Text>
        <Text style={styles.tagline}>Scan • Detect • Enjoy</Text>

        <View style={styles.buttons}>
          <View style={styles.button}>
            <Button title="Choose Photo" onPress={pickImage} />
          </View>
          {photo && (
            <View style={styles.button}>
              <Button
                title={uploading ? 'Analyzing...' : 'Upload & Analyze'}
                onPress={uploadImage}
                disabled={uploading}
              />
            </View>
          )}
        </View>

        {uploading && <ActivityIndicator size="large" style={styles.loader} />}

        {photo?.uri && <Image source={{ uri: photo.uri }} style={styles.image} />}

        {result && (
          <View style={styles.result}>
            <Text style={styles.resultTitle}>Results</Text>
            <Text style={styles.jsonText}>
              {JSON.stringify(result, null, 2)}
            </Text>
          </View>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: {
    flex: 1,
    backgroundColor: '#fff',
  },
  container: {
    flexGrow: 1,
    paddingTop: 40,
    paddingHorizontal: 24,
    alignItems: 'center',
  },
  title: {
    fontSize: 26,
    fontWeight: '700',
    color: '#222',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#555',
    textAlign: 'center',
    marginBottom: 16,
    lineHeight: 22,
  },
  tagline: {
    fontSize: 18,
    fontStyle: 'italic',
    color: '#888',
    marginBottom: 24,
  },
  buttons: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginBottom: 16,
  },
  button: {
    marginHorizontal: 8,
  },
  loader: {
    marginVertical: 20,
  },
  image: {
    width: 280,
    height: 280,
    borderRadius: 8,
    marginVertical: 16,
    backgroundColor: '#eee',
  },
  result: {
    width: '100%',
    backgroundColor: '#f9f9f9',
    padding: 16,
    borderRadius: 6,
    marginBottom: 40,
  },
  resultTitle: {
    fontSize: 18,
    fontWeight: '600',
    marginBottom: 8,
    color: '#333',
  },
  jsonText: {
    fontFamily: 'monospace',
    fontSize: 14,
    color: '#444',
  },
});