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
  Alert,
  TouchableOpacity,
} from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import axios from 'axios';

export default function App() {
  const [photo, setPhoto] = useState<ImagePicker.ImagePickerAsset | null>(null);
  const [result, setResult] = useState<any>(null);
  const [uploading, setUploading] = useState(false);

  // Replace with your actual backend URL
  const BACKEND_URL = 'http://10.0.0.12:4000'; // Update this with your computer's IP

  const pickImage = async () => {
    // Ask for permission
    const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert('Permission denied', 'We need camera roll permissions!');
      return;
    }
    // Launch picker
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      quality: 0.8,
    });
    if (!result.canceled && result.assets && result.assets.length > 0) {
      setPhoto(result.assets[0]);
      setResult(null);
    }
  };

  const takePhoto = async () => {
    // Ask for camera permission
    const { status } = await ImagePicker.requestCameraPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert('Permission denied', 'We need camera permissions!');
      return;
    }
    // Launch camera
    const result = await ImagePicker.launchCameraAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      quality: 0.8,
    });
    if (!result.canceled && result.assets && result.assets.length > 0) {
      setPhoto(result.assets[0]);
      setResult(null);
    }
  };

  const uploadImage = async () => {
    if (!photo?.uri) {
      Alert.alert('Error', 'No photo selected');
      return;
    }
    
    setUploading(true);
    console.log('Uploading photo to:', `${BACKEND_URL}/predict`);

    const formData = new FormData();
    formData.append('file', {
      uri: photo.uri,
      name: photo.fileName || 'photo.jpg',
      type: photo.type || 'image/jpeg',
    } as any);

    try {
      console.log('Sending request...');
      const res = await axios.post(
        `${BACKEND_URL}/predict`,
        formData,
        { 
          headers: { 
            'Content-Type': 'multipart/form-data' 
          },
          timeout: 120000, // 120 second timeout for model loading
        }
      );
      console.log('Response received:', res.data);
      setResult(res.data);
    } catch (error: any) {
      console.error('Upload error:', error);
      let errorMessage = 'Upload failed';
      if (error.response) {
        errorMessage = `Server error: ${error.response.status}`;
      } else if (error.request) {
        errorMessage = 'Network error - check your connection';
      } else {
        errorMessage = error.message || 'Unknown error';
      }
      setResult({ error: errorMessage });
      Alert.alert('Upload Failed', errorMessage);
    } finally {
      setUploading(false);
    }
  };

  const resetApp = () => {
    setPhoto(null);
    setResult(null);
    setUploading(false);
  };

  return (
    <SafeAreaView style={styles.safe}>
      <ScrollView contentContainerStyle={styles.container}>
        <Text style={styles.title}>Grocery Shelf Classifier</Text>
        <Text style={styles.subtitle}>
          Take a photo of your grocery shelf and see what products are detected.
        </Text>
        <Text style={styles.tagline}>Scan • Detect • Enjoy</Text>

        <View style={styles.buttonsRow}>
          <TouchableOpacity style={styles.smallButton} onPress={pickImage}>
            <Text style={styles.buttonText}>Choose Photo</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.smallButton} onPress={takePhoto}>
            <Text style={styles.buttonText}>Take Photo</Text>
          </TouchableOpacity>
          {photo && (
            <TouchableOpacity style={styles.smallButton} onPress={uploadImage} disabled={uploading}>
              <Text style={styles.buttonText}>{uploading ? 'Loading Model & Analyzing...' : 'Upload & Analyze'}</Text>
            </TouchableOpacity>
          )}
        </View>
        <View style={styles.resetRow}>
          <TouchableOpacity style={styles.resetButton} onPress={resetApp}>
            <Text style={styles.resetButtonText}>Reset</Text>
          </TouchableOpacity>
        </View>

        {uploading && <ActivityIndicator size="large" style={styles.loader} />}

        {photo?.uri && (
          <View style={{ alignItems: 'center', justifyContent: 'center' }}>
            <View style={{ width: 280, height: 280, position: 'relative' }}>
              <Image
                source={{ uri: photo.uri }}
                style={styles.image}
              />
              {result?.results?.map((item: any, idx: number) => {
                // Get original image size (fallback to 280x280 if not available)
                const originalWidth = photo.width || 280;
                const originalHeight = photo.height || 280;
                const [xmin, ymin, xmax, ymax] = item.box;
                const scaleX = 280 / originalWidth;
                const scaleY = 280 / originalHeight;
                const left = xmin * scaleX;
                const top = ymin * scaleY;
                const width = (xmax - xmin) * scaleX;
                const height = (ymax - ymin) * scaleY;
                return (
                  <View
                    key={idx}
                    style={{
                      position: 'absolute',
                      left,
                      top,
                      width,
                      height,
                      borderWidth: 2,
                      borderColor: 'red',
                      borderRadius: 4,
                    }}
                  >
                    <Text style={{
                      backgroundColor: 'rgba(255,0,0,0.7)',
                      color: '#fff',
                      fontSize: 10,
                      paddingHorizontal: 2,
                      position: 'absolute',
                      top: -16,
                      left: 0,
                      borderRadius: 2,
                    }}>
                      {item.label} ({(item.confidence * 100).toFixed(1)}%)
                    </Text>
                  </View>
                );
              })}
            </View>
          </View>
        )}

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
  buttonsRow: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginBottom: 16,
    flexWrap: 'wrap',
  },
  smallButton: {
    backgroundColor: '#4a90e2',
    paddingVertical: 8,
    paddingHorizontal: 12,
    borderRadius: 6,
    marginHorizontal: 4,
    marginBottom: 4,
    minWidth: 90,
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontSize: 13,
    fontWeight: '600',
  },
  resetRow: {
    alignItems: 'center',
    marginBottom: 16,
  },
  resetButton: {
    backgroundColor: '#e94e77',
    paddingVertical: 7,
    paddingHorizontal: 18,
    borderRadius: 6,
    marginTop: 8,
  },
  resetButtonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '700',
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