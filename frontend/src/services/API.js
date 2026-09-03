export const scanAPI = {
  getRecent: async () => {
    try {
      return {
        success: true,
        data: [
          { 
            id: '1', 
            website_url: 'https://example.com', 
            created_at: new Date().toISOString() 
          },
          { 
            id: '2', 
            website_url: 'https://google.com', 
            created_at: new Date(Date.now() - 86400000).toISOString() 
          },
        ]
      };
    } catch (error) {
      return { success: false, error: error };
    }
  }
};
