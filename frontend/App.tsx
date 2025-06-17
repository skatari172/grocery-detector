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
          timeout: 30000, // 30 second timeout
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